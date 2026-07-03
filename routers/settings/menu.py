import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import kb_software
from routers.utils import safe_edit

logger = logging.getLogger(__name__)
router = Router()


_SOFTWARE_TEXT = (
    "📖 <b>Настройки ПО</b>\n\n"
    "Знание — оружие. Здесь оно бесплатно.\n\n"
    "Пошаговые руководства со скриншотами.\n"
    "Выбери платформу:"
)

@router.callback_query(F.data == "menu_settings")
async def cb_guides(callback: CallbackQuery) -> None:
    await safe_edit(callback, _SOFTWARE_TEXT, reply_markup=kb_software())