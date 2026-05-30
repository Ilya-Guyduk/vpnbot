import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import kb_software
from handlers.utils import safe_edit

from handlers.software import menu_vpn_clients


logger = logging.getLogger(__name__)
router = Router()
router.include_router(menu_vpn_clients.router)


_SOFTWARE_TEXT = (
    "📖 <b>Софт</b>\n\n"
    "Знание — оружие. Здесь оно бесплатно.\n\n"
    "Пошаговые руководства со скриншотами.\n"
    "Выбери платформу:"
)


@router.callback_query(F.data == "menu_software")
async def cb_guides(callback: CallbackQuery) -> None:
    await safe_edit(callback, _SOFTWARE_TEXT, reply_markup=kb_software())