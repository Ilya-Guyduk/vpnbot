"""
Фоновый polling: каждые 30 секунд проверяет оплату pending-платежей.
Запускается как asyncio-задача в main.py.
"""

import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional
from config import VPN_PLANS
from keyboards.inline import kb_main

from aiogram import Bot

from database import db
from services.cryptobot import get_invoices
from handlers.vpn.payment import PaymentService, parse_payload
from services.xui_panel_api_client.xui_panel_api_client.client import AuthenticatedClient

logger = logging.getLogger(__name__)

POLL_INTERVAL = 3  # секунд


async def payment_poller(bot: Bot, xui_client: AuthenticatedClient) -> None:
    """
    Фоновый поллер для проверки оплат
    
    Аргументы:
        bot: Экземпляр бота для отправки сообщений
        xui_client: Клиент для работы с 3x-ui API
    """
    logger.info("Поллер платежей запущен (интервал %ds)", POLL_INTERVAL)
    
    payment_service = PaymentService(bot, xui_client)
    
    while True:
        try:
            await _poll_once(bot, payment_service)
        except Exception as exc:
            logger.exception("Ошибка в поллере: %s", exc)
        await asyncio.sleep(POLL_INTERVAL)


async def _poll_once(bot: Bot, payment_service: PaymentService) -> None:
    """Одна итерация поллера"""
    # Получаем все pending платежи
    pending = db.get_pending_payments()
    if not pending:
        return

    invoice_ids = [row["crypto_invoice_id"] for row in pending]
    logger.debug("Проверяем %d pending-платежей: %s", len(invoice_ids), invoice_ids)

    # Получаем статусы инвойсов из CryptoBot
    invoices = await get_invoices(invoice_ids)
    inv_map = {inv.invoice_id: inv for inv in invoices}

    # Чистим просроченные платежи (старше 2 часов)
    expired_count = db.expire_old_pending_payments(older_than_hours=2)
    if expired_count:
        logger.info("Помечено как expired: %d платежей", expired_count)

    for row in pending:
        inv = inv_map.get(row["crypto_invoice_id"])
        if not inv:
            continue

        if inv.status == "paid":
            logger.info(
                "Оплата найдена поллером: payment_id=%s invoice_id=%s user_id=%s",
                row["id"], inv.invoice_id, row["user_id"]
            )
            
            try:
                # Парсим payload для получения plan_id
                plan_id, _ = parse_payload(inv.payload)
                # В новой структуре нет parent_tunnel_id, так как мы не храним туннели
                parent_tunnel_id = None
            except (ValueError, AttributeError):
                # Если не удалось распарсить, используем значения по умолчанию
                plan_id = list(VPN_PLANS.keys())[0] if VPN_PLANS else "basic"
                parent_tunnel_id = None
                logger.warning("Не удалось распарсить payload для payment %s", row["id"])
            
            # Рассчитываем дату окончания подписки
            duration_days = row["duration_days"]
            expires_at = datetime.now() + timedelta(days=duration_days)
            
            # Отмечаем платеж как оплаченный
            db.mark_payment_paid(row["id"], expires_at)
            
            # Обрабатываем активацию туннеля через сервис
            success = await payment_service.process_payment(
                payment_id=row["id"],
                user_id=row["user_id"],
                plan_id=plan_id,
                duration_days=duration_days,
                expires_at=expires_at,
                parent_tunnel_id=None  # В новой версии не используем
            )
            
            if success:
                logger.info("Туннель успешно активирован для payment %s", row["id"])
                await _notify_payment_success(bot, row["user_id"], expires_at)
            else:
                logger.error("Не удалось активировать туннель для payment %s", row["id"])
                await _notify_payment_failed(bot, row["user_id"])

        elif inv.status == "expired":
            db.mark_payment_expired(row["id"])
            logger.info("Invoice %s истёк, payment %s → expired", inv.invoice_id, row["id"])
            
            # Уведомляем пользователя об истечении счёта
            await _notify_payment_expired(bot, row["user_id"])


# ── Вспомогательные функции для уведомлений ─────────────────────────────────

async def _notify_payment_success(bot: Bot, user_id: int, expires_at: datetime) -> None:
    """Уведомление об успешной оплате"""
    try:
        expires_str = expires_at.strftime("%d.%m.%Y %H:%M")
        await bot.send_message(
            user_id,
            f"✅ **Оплата прошла успешно!**\n\n"
            f"🎉 Подписка активирована до: `{expires_str}`\n"
            f"Теперь вы можете использовать VPN.",
            reply_markup=kb_main()
        )
    except Exception as e:
        logger.warning("Не удалось уведомить пользователя %s об успешной оплате: %s", 
                      user_id, e)


async def _notify_payment_failed(bot: Bot, user_id: int) -> None:
    """Уведомление о неудачной активации"""
    try:
        await bot.send_message(
            user_id,
            "⚠️ **Ошибка активации подписки**\n\n"
            "Оплата прошла успешно, но возникла ошибка при активации VPN.\n"
            "Пожалуйста, обратитесь в поддержку.",
            reply_markup=kb_main()
        )
    except Exception as e:
        logger.warning("Не удалось уведомить пользователя %s об ошибке: %s", 
                      user_id, e)


async def _notify_payment_expired(bot: Bot, user_id: int) -> None:
    """Уведомление об истечении счёта"""
    try:
        await bot.send_message(
            user_id,
            "❌ **Счёт на оплату истёк**\n\n"
            "Время ожидания оплаты вышло.\n"
            "Создайте новый заказ в разделе «Купить VPN».",
            reply_markup=kb_main()
        )
    except Exception as e:
        logger.warning("Не удалось уведомить пользователя %s об истечении: %s", 
                      user_id, e)