"""
Оплата через CryptoBot (@CryptoBot / @CryptoTestnetBot).

Флоу:
  buy_vpn_<plan_id>    → createInvoice → кнопка «Оплатить»
  check_payment_<id>   → getInvoices   → при paid → Ansible → конфиг
  [фоновый poller]     → то же самое автоматически каждые 30с
"""

import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import VPN_PLANS, ADMIN_IDS, CRYPTO_ASSET, CRYPTO_BOT_TOKEN
from database import db
from keyboards.inline import kb_main
from services.cryptobot import create_invoice, get_invoices

logger = logging.getLogger(__name__)
router = Router()

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


# ── 1. Пользователь выбирает тариф ──────────────────────────────────────────

@router.callback_query(F.data.startswith("buy_vpn_"))
async def cb_buy_vpn(callback: CallbackQuery) -> None:
    if not CRYPTO_BOT_TOKEN:
        await callback.answer("⚠️ Оплата временно недоступна", show_alert=True)
        return

    plan_id = callback.data.removeprefix("buy_vpn_")
    if plan_id not in VPN_PLANS:
        await callback.answer("❌ Тариф не найден", show_alert=True)
        return

    plan = VPN_PLANS[plan_id]
    await callback.answer("⏳ Создаём счёт...")

    # Создаём pending-заказ в БД (invoice_id обновим после ответа API)
    order_id = db.create_order(
        user_id=callback.from_user.id,
        duration_days=plan["duration"],
        crypto_invoice_id=0,
        crypto_asset=CRYPTO_ASSET,
        amount_crypto=str(plan["price"]),
    )

    invoice = await create_invoice(
        amount=plan["price"],
        asset=CRYPTO_ASSET,
        description=plan["name"] + " · VPN-подписка",
        payload=_make_payload(plan_id, order_id),
        expires_in=3600,
    )

    if not invoice:
        db.fail_order(order_id)
        await callback.message.answer(
            "❌ Не удалось создать счёт. Попробуйте позже или обратитесь в @support"
        )
        return

    # Сохраняем реальный invoice_id
    with db.get_db() as conn:
        conn.execute(
            "UPDATE orders SET crypto_invoice_id=? WHERE id=?",
            (invoice.invoice_id, order_id),
        )

    logger.info(
        "Invoice created: plan=%s order_id=%s invoice_id=%s %s %s",
        plan_id, order_id, invoice.invoice_id, invoice.amount, invoice.asset,
    )

    plan_name = plan["name"]
    text = (
        "💳 <b>Счёт на оплату</b>\n\n"
        f"📦 <b>Тариф:</b> {plan_name}\n"
        f"💰 <b>Сумма:</b> {invoice.amount} {invoice.asset}\n"
        "⏳ <b>Действует:</b> 1 час\n\n"
        "Нажмите кнопку ниже — откроется @CryptoBot для оплаты.\n"
        "После оплаты нажмите <b>«Проверить оплату»</b>."
    )

    b = InlineKeyboardBuilder()
    b.button(
        text=f"💳 Оплатить {invoice.amount} {invoice.asset}",
        url=invoice.pay_url,
    )
    b.button(text="🔄 Проверить оплату",  callback_data=f"check_payment_{order_id}")
    b.button(text="◀️ Назад к тарифам",   callback_data="menu_vpn")
    b.adjust(1)

    await callback.message.edit_text(text, reply_markup=b.as_markup())


# ── 2. Пользователь нажимает «Проверить оплату» ──────────────────────────────

@router.callback_query(F.data.startswith("check_payment_"))
async def cb_check_payment(callback: CallbackQuery, bot: Bot) -> None:
    try:
        order_id = int(callback.data.removeprefix("check_payment_"))
    except ValueError:
        await callback.answer("❌ Неверный ID заказа", show_alert=True)
        return

    await callback.answer("🔄 Проверяем статус...")

    with db.get_db() as conn:
        row = conn.execute(
            "SELECT * FROM orders WHERE id=? AND user_id=?",
            (order_id, callback.from_user.id),
        ).fetchone()

    if not row:
        await callback.answer("❌ Заказ не найден", show_alert=True)
        return

    if row["status"] == "paid":
        await callback.answer("✅ Уже оплачено — конфиг был отправлен ранее.", show_alert=True)
        return

    if row["status"] in ("failed", "expired"):
        await callback.answer("❌ Счёт истёк. Пожалуйста, создайте новый.", show_alert=True)
        return

    invoices = await get_invoices([row["crypto_invoice_id"]])
    if not invoices:
        await callback.answer("⚠️ Не удалось проверить статус. Попробуйте позже.", show_alert=True)
        return

    inv = invoices[0]

    if inv.status == "paid":
        await callback.answer("✅ Оплата найдена! Настраиваем VPN...")
        await _deliver_vpn(bot, callback.from_user.id, order_id, row, inv)
    elif inv.status == "expired":
        db.fail_order(order_id)
        await callback.answer("❌ Счёт истёк. Создайте новый заказ.", show_alert=True)
    else:
        await callback.answer(
            "⏳ Оплата ещё не поступила. Попробуйте через минуту.",
            show_alert=True,
        )


# ── 3. Доставка конфига (используется и поллером, и ручной проверкой) ────────

async def _deliver_vpn(bot: Bot, user_id: int, order_id: int, order_row, inv) -> None:
    from services.ansible import provision_vpn_user

    plan_id, _ = _parse_payload(inv.payload)
    if not plan_id or plan_id not in VPN_PLANS:
        logger.error("Не распознан payload=%s order_id=%s", inv.payload, order_id)
        return

    plan = VPN_PLANS[plan_id]
    plan_name = plan["name"]

    wait_msg = await bot.send_message(
        user_id,
        "⏳ Оплата подтверждена! Настраиваем сервер — до 2 минут...",
    )

    vpn_config = await provision_vpn_user(user_id, plan["duration"])

    if vpn_config:
        db.complete_order(order_id, vpn_config, plan["duration"], user_id)
        await wait_msg.delete()
        await bot.send_message(
            user_id,
            "✅ <b>Ваш VPN готов!</b>\n\n"
            "<b>Конфигурация:</b>\n"
            f"<code>{vpn_config}</code>\n\n"
            "📖 Как подключиться — раздел <b>«Руководства»</b> в меню.\n"
            "По вопросам: @support",
            reply_markup=kb_main(),
        )
        await _notify_admins(
            bot,
            f"💰 Новая продажа (CryptoBot)\n"
            f"User: {user_id}\n"
            f"Тариф: {plan_name}\n"
            f"Сумма: {inv.amount} {inv.asset}\n"
            f"Order: {order_id} | Invoice: {inv.invoice_id}",
        )
    else:
        db.fail_order(order_id)
        await wait_msg.delete()
        await bot.send_message(
            user_id,
            "❌ Не удалось подготовить конфиг. Администраторы уведомлены.\n"
            "Поддержка: @support",
            reply_markup=kb_main(),
        )
        await _notify_admins(
            bot,
            f"⚠️ Ошибка Ansible!\n"
            f"User: {user_id} | Order: {order_id}\n"
            f"Invoice: {inv.invoice_id} | Оплата прошла, конфиг не создан!",
        )


async def _notify_admins(bot: Bot, text: str) -> None:
    for admin_id in ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception as exc:
            logger.warning("Не удалось уведомить admin %s: %s", admin_id, exc)
