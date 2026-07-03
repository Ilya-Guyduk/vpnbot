import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import kb_guides
from routers.utils import safe_edit
from routers.guides import guides

logger = logging.getLogger(__name__)
router = Router()
router.include_router(guides.router)



_GUIDES_TEXT = (
    "📖 <b>Инструкции</b>\n\n"
    "Знание — оружие. Здесь оно бесплатно.\n\n"
    "Пошаговые руководства со скриншотами.\n"
    "Выбери платформу:"
)


@router.callback_query(F.data == "menu_guides")
async def cb_guides(callback: CallbackQuery) -> None:
    await safe_edit(callback, _GUIDES_TEXT, reply_markup=kb_guides())