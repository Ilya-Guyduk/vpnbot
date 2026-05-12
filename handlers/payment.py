"""
Оплата через Telegram Stars (currency=XTR).

Флоу:
  buy_vpn_<plan_id>  →  send_invoice (Stars)
  pre_checkout_query →  подтверждение
  successful_payment →  запуск Ansible → выдача конфига
"""

import logging
from aiogram import Router, F, Bot
from aiogram.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)

from config import VPN_PLANS, ADMIN_IDS
from database import db
from keyboards.inline import kb_main
from services.ansible import provision_vpn_user

logger = logging.getLogger(__name__)
router = Router()

# Разделитель payload: vpn|<plan_id>|<order_id>
_SEP = "|"


def _make_payload(plan_id: str, order_id: int) -> str:
    return f"vpn{_SEP}{plan_id}{_SEP}{order_id}"


def _parse_payload(payload: str) -> tuple[str, int] | tuple[None, None]:
    parts = payload.split(_SEP)
    if len(parts) != 3 or parts[0] != "vpn":
        return None, None
    try:
        return parts[1], int(parts[2])
    except ValueError:
        return None, None


# ── 1. Выбор тарифа ─────────────────────────────────────────────────────────

@router.callback_query(F.data.startswith("buy_vpn_"))
async def cb_buy_vpn(callback: CallbackQuery, bot: Bot) -> None:
    plan_id = callback.data.removeprefix("buy_vpn_")

    if plan_id not in VPN_PLANS:
        await callback.answer("❌ Тариф не найден", show_alert=True)
        return

    plan = VPN_PLANS[plan_id]

    # Создаём заказ заранее, чтобы иметь order_id для payload
    order_id = db.create_order(
        user_id=callback.from_user.id,
        amount_stars=plan["price_stars"],
        duration_days=plan["duration"],
    )
    logger.info(f"send_invoice plan_id:{plan_id}, plan{plan}, order_id:{order_id}, price:{LabeledPrice(label=plan["name"], amount=plan["price_stars"])}")

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=plan["name"],
        description="VPN-подписка для обхода цензуры",
        payload=_make_payload(plan_id, order_id),
        currency="XTR",          # Telegram Stars — без provider_token
        prices=[LabeledPrice(label=plan["name"], amount=plan["price_stars"])],
    )
    await callback.answer("⭐ Счёт отправлен")


# ── 2. Pre-checkout ──────────────────────────────────────────────────────────

@router.pre_checkout_query()
async def cb_pre_checkout(pre_checkout: PreCheckoutQuery, bot: Bot) -> None:
    logger.debug(f"cb_pre_checkout()")
    plan_id, order_id = _parse_payload(pre_checkout.invoice_payload)

    if plan_id is None or plan_id not in VPN_PLANS:
        await bot.answer_pre_checkout_query(
            pre_checkout.id,
            ok=False,
            error_message="❌ Ошибка обработки заказа. Попробуйте позже.",
        )
        return

    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)


# ── 3. Успешная оплата ───────────────────────────────────────────────────────

@router.message(F.successful_payment)
async def cb_successful_payment(message: Message, bot: Bot) -> None:
    payment = message.successful_payment
    plan_id, order_id = _parse_payload(payment.invoice_payload)

    if plan_id is None or plan_id not in VPN_PLANS:
        logger.error(
            "Неизвестный payload после оплаты: %s (user=%s)",
            payment.invoice_payload, message.from_user.id,
        )
        await message.answer(
            "❌ Ошибка при обработке платежа. Свяжитесь с поддержкой: @support",
            reply_markup=kb_main(),
        )
        await _notify_admins(
            bot,
            f"⚠️ КРИТИЧЕСКАЯ ОШИБКА\n"
            f"Оплата прошла, но payload не распознан.\n"
            f"User: {message.from_user.id} | Payload: {payment.invoice_payload}\n"
            f"Stars: {payment.total_amount}",
        )
        return

    plan = VPN_PLANS[plan_id]

    # Сообщаем пользователю, что идёт настройка (может занять время)
    wait_msg = await message.answer(
        "⏳ Оплата получена! Настраиваем ваш VPN-сервер — займёт до 2 минут..."
    )

    vpn_config = await provision_vpn_user(message.from_user.id, plan["duration"])

    if vpn_config:
        db.complete_order(
            order_id=order_id,
            telegram_charge_id=payment.telegram_payment_charge_id,
            vpn_config=vpn_config,
            duration_days=plan["duration"],
            user_id=message.from_user.id,
        )

        await wait_msg.delete()
        await message.answer(
            f"✅ <b>Ваш VPN готов!</b>\n\n"
            f"<b>Конфигурация для подключения:</b>\n"
            f"<code>{vpn_config}</code>\n\n"
            f"📖 Как подключиться — раздел <b>«Руководства»</b> в меню.\n"
            f"По вопросам: @support",
            reply_markup=kb_main(),
        )

        await _notify_admins(
            bot,
            f"💰 Новая продажа (Stars)\n"
            f"User: @{message.from_user.username} ({message.from_user.id})\n"
            f"Тариф: {plan['name']}\n"
            f"Stars: {payment.total_amount}\n"
            f"Order ID: {order_id}",
        )
    else:
        db.fail_order(order_id)
        await wait_msg.delete()
        await message.answer(
            "❌ Не удалось подготовить VPN-конфиг. "
            "Администраторы уже уведомлены — свяжемся в ближайшее время.\n"
            "Поддержка: @support",
            reply_markup=kb_main(),
        )
        await _notify_admins(
            bot,
            f"⚠️ Ошибка Ansible!\n"
            f"User: {message.from_user.id} | Order: {order_id}\n"
            f"Тариф: {plan['name']} | Stars: {payment.total_amount}\n"
            f"Конфиг не создан — проверить плейбук!",
        )


async def _notify_admins(bot: Bot, text: str) -> None:
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception as exc:
            logger.warning("Не удалось уведомить администратора %s: %s", admin_id, exc)
