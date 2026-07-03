"""Главное меню и навигация."""

import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery


from config import (
    SOFTWARE_MENU_ENABLED, VPN_MENU_ENABLED, GUIDES_MENU_ENABLED,
    SETTINGS_MENU_ENABLED, LINKS_MENU_ENABLED, BOTS_MENU_ENABLED,
    MIRRORS_MENU_ENABLED, HELP_MENU_ENABLED,
)
from keyboards.inline import kb_main

from routers.personal_accont import main as personal_accont
from routers.software import menu as software
from routers.guides import menu as guides
from routers.help import menu as help
from routers.settings import menu as settings

from data.quotes import random_quote

logger = logging.getLogger(__name__)
router = Router()

if VPN_MENU_ENABLED:
    router.include_router(personal_accont.router)
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


# ── Команды ──────────────────────────────────────────────────────────────────

@router.message(Command("start", "menu"))
async def cmd_start(message: Message):
    quote, author = random_quote()
    text = (
        f"👤 <b>Приветствуем, {message.from_user.first_name}.</b>\n\n"
        f"<i>«{quote}»</i>\n"
        f"<b>— {author}</b>\n\n"
        "——————————————————\n"
        "Выбери раздел:"
    )
    await message.answer(text, reply_markup=kb_main())

# ── Навигация ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu_main")
async def cb_main(callback: CallbackQuery) -> None:
    await cmd_start(callback.message)
    return


