"""Главное меню и навигация."""

import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from config import SOFTWARE_MENU_ENABLED, VPN_MENU_ENABLED, GUIDES_MENU_ENABLED, SETTINGS_MENU_ENABLED, LINKS_MENU_ENABLED, BOTS_MENU_ENABLED, MIRRORS_MENU_ENABLED, HELP_MENU_ENABLED
from database.db import register_user, get_active_subscription
from keyboards.inline import kb_main

from handlers.vpn import menu as vpn
from handlers.software import menu as software
from handlers.guides import menu as guides
from handlers.help import menu as help
from handlers.settings import menu as settings

from handlers.utils import safe_edit
from data.quotes import random_quote

logger = logging.getLogger(__name__)
router = Router()

if VPN_MENU_ENABLED:
    router.include_router(vpn.router)
if SOFTWARE_MENU_ENABLED:
    router.include_router(software.router)
if GUIDES_MENU_ENABLED:
    router.include_router(guides.router)
if SETTINGS_MENU_ENABLED:
    router.include_router(settings.router)
if LINKS_MENU_ENABLED:
    router.include_router(links.router)
if BOTS_MENU_ENABLED:
    router.include_router(bots.router)
if MIRRORS_MENU_ENABLED:
    router.include_router(mirrors.router)
if HELP_MENU_ENABLED:
    router.include_router(help.router)

# ── Тексты ───────────────────────────────────────────────────────────────────

def _welcome_text(first_name: str) -> str:
    quote, author = random_quote()
    return (
        f"👤 <b>{first_name}.</b>\n\n"
        "Добро пожаловать в <b>Black List</b>.\n\n"
        f"<i>«{quote}»</i>\n"
        f"<b>— {author}</b>\n\n"
        "——————————————————\n"
        "Выбери раздел:"
    )


def _welcome_text_with_sub(first_name: str, sub_end: datetime) -> str:
    days_left = (sub_end - datetime.now()).days
    if days_left > 7:
        status = f"🟢 Активен · осталось <b>{days_left} дн.</b>"
    elif days_left > 0:
        status = f"🟡 Истекает через <b>{days_left} дн.</b> — продли до отключения"
    else:
        status = "🔴 Истёк — ты снова за Стеной"

    quote, author = random_quote()
    return (
        f"👤 <b>Приветствуем, {first_name}.</b>\n\n"
        f"📡 <b>Статус туннеля:</b> {status}\n\n"
        f"<i>«{quote}»</i>\n"
        f"<b>— {author}</b>\n\n"
        "——————————————————\n"
        "Выбери раздел:"
    )


# ── Утилиты ──────────────────────────────────────────────────────────────────

def _get_welcome(user_id: int, first_name: str) -> str:
    row = get_active_subscription(user_id)
    if row and row["subscription_end"]:
        try:
            sub_end = datetime.fromisoformat(row["subscription_end"])
            return _welcome_text_with_sub(first_name, sub_end)
        except (ValueError, KeyError):
            pass
    return _welcome_text(first_name)


# ── Команды ──────────────────────────────────────────────────────────────────

@router.message(Command("start", "menu"))
async def cmd_start(message: Message) -> None:
    register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
    )
    first_name = message.from_user.first_name or "агент"
    text = _get_welcome(message.from_user.id, first_name)
    await message.answer(text, reply_markup=kb_main())


# ── Навигация ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu_main")
async def cb_main(callback: CallbackQuery) -> None:
    first_name = callback.from_user.first_name or "агент"
    text = _get_welcome(callback.from_user.id, first_name)
    await safe_edit(callback, text, reply_markup=kb_main())