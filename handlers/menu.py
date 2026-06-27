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

from handlers.vpn import menu as vpn
from handlers.software import menu as software
from handlers.guides import menu as guides
from handlers.help import menu as help
from handlers.settings import menu as settings

from services.xui_panel_api_client.xui_panel_api_client.client import AuthenticatedClient
from services.xui_panel_api_client.xui_panel_api_client.api.clients.get_panel_api_clients_get_email import (
    asyncio as get_client,
) 

from services.xui_panel_api_client.xui_panel_api_client.api.clients.get_panel_api_clients_sub_links_sub_id import (
    asyncio as get_client_sub,
)

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


# ── Команды ──────────────────────────────────────────────────────────────────

@router.message(Command("start", "menu"))
async def cmd_start(message: Message, xui_client: AuthenticatedClient):

    tunnel_info = ""

    try:
        result = await get_client(
            email=str(message.from_user.id),
            client=xui_client,
        )

        logger.info(f"res obj: {result}")
        tunnel_info = format_client_info(result)
            

    except Exception:
        logger.exception("XUI request failed")

    quote, author = random_quote()

    text = (
        f"👤 <b>Приветствуем, {message.from_user.first_name}.</b>\n\n"
        f"{tunnel_info}\n\n"
        f"<i>«{quote}»</i>\n"
        f"<b>— {author}</b>\n\n"
        "——————————————————\n"
        "Выбери раздел:"
    )

    await message.answer(text, reply_markup=kb_main())


# ── Навигация ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu_main")
async def cb_main(callback: CallbackQuery) -> None:
    await cmd_start(callback, reply_markup=kb_main())



def format_client_info(client_data: dict | None) -> str:
    if not client_data:
        return (
            "📡 <b>Туннель</b>\n\n"
            "❌ У вас нет активной подписки.\n\n"
            "Нажмите «VPN», чтобы оформить доступ."
        )
    client_data = client_data.obj
    client = client_data["client"]

    traffic_gb = round(
        client_data.get("usedTraffic", 0) / 1024**3,
        2
    )
    
    group = client.get("group") or "не указана"
    enabled = client.get("enable", False)

    expiry = client.get("expiryTime", 0)

    if expiry and expiry > 0:
        expire_dt = datetime.fromtimestamp(expiry / 1000)
        days_left = (expire_dt - datetime.now()).days

        if days_left > 7:
            icon = "🟢"
        elif days_left > 0:
            icon = "🟡"
        else:
            icon = "🔴"

        expiry_text = (
            f"{icon} <b>{expire_dt:%d.%m.%Y}</b>"
            f" ({days_left} дн.)"
        )

    else:
        expiry_text = "♾️ Без ограничений"

    return (
        "📡 <b>Ваш туннель</b>\n\n"
        f"👥 Группа: <b>{group}</b>\n"
        f"📊 Использовано: <b>{traffic_gb:.2f} GB</b>\n"
        f"📅 Действует до: {expiry_text}\n"
        f"🔐 Статус: {'🟢 Активен' if enabled else '🔴 Отключён'}"
    )
