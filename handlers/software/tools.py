"""Инструменты обхода цензуры."""

from aiogram import Router, F
from aiogram import types
from aiogram.types import CallbackQuery
from keyboards.inline import kb_back_tools

router = Router()

_TOOL_INFO: dict[str, str] = {
    "tor": (
        "🌐 <b>Tor Browser</b>\n\n"
        "Маршрутизирует трафик через несколько слоёв шифрования.\n\n"
        "Скачать: torproject.org/download/\n"
        "На русском: torproject.org/ru/download/"
    ),
    "mirrors": (
        "🔄 <b>Зеркала заблокированных сайтов</b>\n\n"
        "Отправьте боту название сайта, чтобы получить актуальное зеркало."
    ),
    "dns": (
        "🔧 <b>Настройка DNS</b>\n\n"
        "Защищённые DNS-серверы для обхода блокировок:\n"
        "• Cloudflare: <code>1.1.1.1</code>\n"
        "• Quad9: <code>9.9.9.9</code>\n"
        "• AdGuard DNS: <code>94.140.14.14</code>"
    ),
    "proxy": (
        "🌍 <b>Прокси-серверы</b>\n\n"
        "Рекомендуемые расширения:\n"
        "• Proxy SwitchyOmega (Chrome/Firefox)\n"
        "• FoxyProxy (Firefox)\n\n"
        "Актуальный список: @proxy_list"
    ),
}


@router.callback_query(F.data.startswith("tool_"))
async def cb_tool_info(callback: CallbackQuery) -> None:
    tool = callback.data.removeprefix("tool_")
    text = _TOOL_INFO.get(tool, "ℹ️ Информация временно недоступна")
    await callback.message.edit_text(
        text,
        reply_markup=kb_back_tools(),
        link_preview_options=types.LinkPreviewOptions(is_disabled=True),
    )
    await callback.answer()
