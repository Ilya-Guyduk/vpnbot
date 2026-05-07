"""Команды администратора."""

import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from config import ADMIN_IDS
from database.db import get_stats

logger = logging.getLogger(__name__)
router = Router()


def _is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS


@router.message(Command("admin"))
async def cmd_admin(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        await message.answer("⛔️ Доступ запрещён")
        return

    await message.answer(
        "👨‍💼 <b>Админ-панель</b>\n\n"
        "Команды:\n"
        "/stats — статистика\n"
        "/broadcast — рассылка (в разработке)"
    )


@router.message(Command("stats"))
async def cmd_stats(message: Message) -> None:
    if not _is_admin(message.from_user.id):
        return

    s = get_stats()
    await message.answer(
        f"📊 <b>Статистика</b>\n\n"
        f"👥 Пользователей: {s['total_users']}\n"
        f"💰 Оплаченных заказов: {s['total_orders']}\n"
        f"⭐ Всего Stars получено: {s['total_stars']}"
    )


@router.message(Command("my_key"))
async def cmd_my_key(message: Message) -> None:
    """Просмотр активного VPN-конфига."""
    from database.db import get_active_subscription
    from datetime import datetime

    row = get_active_subscription(message.from_user.id)

    if not row:
        await message.answer(
            "У вас нет активной подписки. "
            "Приобретите её в разделе <b>VPN-сервисы</b>."
        )
        return

    sub_end = datetime.fromisoformat(row["subscription_end"])
    days_left = (sub_end - datetime.now()).days

    if days_left <= 0:
        await message.answer(
            "⚠️ Ваша подписка истекла. Приобретите новую в разделе VPN."
        )
        return

    await message.answer(
        f"✅ <b>Подписка активна</b>\n\n"
        f"🔑 Конфиг:\n<code>{row['vpn_config']}</code>\n\n"
        f"📅 Действует до: {sub_end.strftime('%d.%m.%Y')}\n"
        f"⏳ Осталось дней: {days_left}"
    )
