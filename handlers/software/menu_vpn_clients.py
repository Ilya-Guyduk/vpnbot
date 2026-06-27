import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from data.vpn_clients import VPN_CLIENTS, ICONS
from handlers.utils import safe_edit
from keyboards.inline import (
    kb_vpn_clients,
    kb_vpn_client_platforms,
    kb_vpn_client_versions,
)

logger = logging.getLogger(__name__)
router = Router()


_SOFTWARE_TEXT = (
    "📖 <b>VPN-клиенты</b>\n\n"
    "Знание — оружие. Здесь оно бесплатно.\n\n"
    "Пошаговые руководства со скриншотами.\n"
    "Выбери платформу:"
)


@router.callback_query(F.data == "menu_vpn_clients")
async def cb_vpn_clients(callback: CallbackQuery):
    await safe_edit(
        callback,
        _SOFTWARE_TEXT,
        reply_markup=kb_vpn_clients()
    )


@router.callback_query(F.data.startswith("vpn_client:"))
async def cb_vpn_client(callback: CallbackQuery):
    client_id = callback.data.split(":")[1]

    client = VPN_CLIENTS.get(client_id)

    if not client:
        return

    icons = "".join(
        ICONS[p]
        for p in client["platforms"]
    )

    protocols = ", ".join(client["protocols"])

    text = (
        f"{icons} <b>{client['name']}</b>\n\n"
        f"{client['description']}\n\n"
        f"<b>Протоколы:</b>\n"
        f"{protocols}\n\n"
        f"Выберите платформу:"
    )

    await safe_edit(
        callback,
        text,
        reply_markup=kb_vpn_client_platforms(client_id)
    )

@router.callback_query(
    F.data.startswith("vpn_platform:")
)
async def cb_vpn_platform(callback: CallbackQuery):
    _, client_id, platform = callback.data.split(":")

    client = VPN_CLIENTS[client_id]
    version = client["versions"][platform]

    text = (
        f"{ICONS[platform]} "
        f"<b>{client['name']} — "
        f"{platform.capitalize()}</b>\n\n"
        f"<b>Версия:</b>\n"
        f"{version['label']}\n"
    )

    if note := version.get("note"):
        text += f"\n<b>Примечание:</b>\n{note}"

    text += "\n\nНажмите кнопку ниже для скачивания."

    await safe_edit(
        callback,
        text,
        reply_markup=kb_vpn_client_versions(
            client_id,
            platform,
        )
    )