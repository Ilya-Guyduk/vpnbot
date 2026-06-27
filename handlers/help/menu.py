import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import kb_back_main
from handlers.utils import safe_edit

logger = logging.getLogger(__name__)
router = Router()


_HELP_TEXT = (
    "❓ <b>Как это работает</b>\n\n"
    "<b>Получить туннель (VPN):</b>\n"
    "  1. Раздел «Black List VPN» → выбери тариф\n"
    "  2. Оплати криптой через CryptoBot\n"
    "  3. Получи конфиг — готово\n\n"
    "<b>Бесплатные инструменты:</b>\n"
    "  → Прокси, DNS, Tor — без регистрации\n\n"
    "<b>Подключение:</b>\n"
    "  → Раздел «Инструкции»\n\n"
    "——————————————————\n"
    "💬 Связь с оператором: @support\n"
    "⏱ Ответ: до 2 часов\n\n"
    "<i>Если бот недоступен — нас заблокировали.\n"
    "Резервный контакт: @blacklist_reserve</i>"
)

@router.callback_query(F.data == "menu_help")
async def cb_help(callback: CallbackQuery) -> None:
    await safe_edit(callback, _HELP_TEXT, reply_markup=kb_back_main())