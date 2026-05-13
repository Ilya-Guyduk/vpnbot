"""
Фоновый polling: каждые 30 секунд проверяет оплату pending-заказов.
Запускается как asyncio-задача в main.py.
"""

import asyncio
import logging
from aiogram import Bot

from database import db
from services.cryptobot import get_invoices
from handlers.payment import _deliver_vpn

logger = logging.getLogger(__name__)

POLL_INTERVAL = 30  # секунд


async def payment_poller(bot: Bot) -> None:
    logger.info("Поллер платежей запущен (интервал %ds)", POLL_INTERVAL)
    while True:
        try:
            await _poll_once(bot)
        except Exception as exc:
            logger.exception("Ошибка в поллере: %s", exc)
        await asyncio.sleep(POLL_INTERVAL)


async def _poll_once(bot: Bot) -> None:
    pending = db.get_pending_crypto_orders()
    if not pending:
        return

    invoice_ids = [row["crypto_invoice_id"] for row in pending]
    logger.debug("Проверяем %d pending-заказов: %s", len(invoice_ids), invoice_ids)

    invoices = await get_invoices(invoice_ids)
    inv_map = {inv.invoice_id: inv for inv in invoices}

    # Чистим просроченные заказы
    expired_count = db.expire_old_pending_orders(older_than_hours=2)
    if expired_count:
        logger.info("Помечено как expired: %d заказов", expired_count)

    for row in pending:
        inv = inv_map.get(row["crypto_invoice_id"])
        if not inv:
            continue

        if inv.status == "paid":
            logger.info(
                "Оплата найдена поллером: order_id=%s invoice_id=%s",
                row["id"], inv.invoice_id,
            )
            await _deliver_vpn(bot, row["user_id"], row["id"], row, inv)

        elif inv.status == "expired":
            db.fail_order(row["id"])
            logger.info("Invoice %s истёк, order %s → expired", inv.invoice_id, row["id"])
