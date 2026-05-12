"""Главное меню и навигация."""

import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.db import register_user, get_active_subscription
from keyboards.inline import kb_main, kb_vpn_plans, kb_tools, kb_guides, kb_back_main, kb_vpn_cliients

logger = logging.getLogger(__name__)
router = Router()


# ── Тексты ───────────────────────────────────────────────────────────────────

def _welcome_text(first_name: str) -> str:
    return (
        f"👋 <b>Привет, {first_name}!</b>\n\n"
        "🛡 <b>Свободный интернет — это просто.</b>\n\n"
        "Этот бот поможет вам обойти любые блокировки:\n\n"
        "  🔒 <b>VPN</b> — надёжные серверы, оплата в Stars\n"
        "  🌐 <b>Tor & Прокси</b> — анонимность без регистрации\n"
        "  🔄 <b>Зеркала</b> — актуальные ссылки на заблокированные сайты\n"
        "  📖 <b>Руководства</b> — пошаговые инструкции для любой платформы\n\n"
        "Выберите раздел:"
    )


def _welcome_text_with_sub(first_name: str, sub_end: datetime) -> str:
    days_left = (sub_end - datetime.now()).days
    if days_left > 7:
        status = f"✅ Активна · осталось <b>{days_left} дн.</b>"
    elif days_left > 0:
        status = f"⚠️ Истекает через <b>{days_left} дн.</b> — пора продлить"
    else:
        status = "🔴 Истекла — оформите новую подписку"

    return (
        f"👋 <b>С возвращением, {first_name}!</b>\n\n"
        f"📡 <b>Подписка:</b> {status}\n\n"
        "Выберите раздел:"
    )


_VPN_TEXT = (
    "🔒 <b>VPN-сервисы</b>\n\n"
    "Выберите тариф — после оплаты Stars бот автоматически "
    "настроит сервер и пришлёт конфиг.\n\n"
    "⚡ Среднее время активации: <b>~60 секунд</b>\n"
    "🌍 Серверы в юрисдикциях без цензуры\n"
    "🔑 Один ключ — все устройства"
)


_SOFTWARE_TEXT = (
    "🛠 <b>Инструменты обхода цензуры</b>\n\n"
    "Бесплатные альтернативы VPN — работают без регистрации:"
)

_GUIDES_TEXT = (
    "📖 <b>Руководства по настройке</b>\n\n"
    "Пошаговые инструкции со скриншотами.\n"
    "Выберите вашу платформу:"
)

_HELP_TEXT = (
    "❓ <b>Как это работает</b>\n\n"
    "<b>VPN-подписка:</b>\n"
    "  1. Выберите тариф в разделе VPN\n"
    "  2. Оплатите через Telegram Stars\n"
    "  3. Получите конфиг — готово!\n\n"
    "<b>Бесплатные инструменты:</b>\n"
    "  → Раздел «Другие инструменты»\n\n"
    "<b>Как подключиться:</b>\n"
    "  → Раздел «Руководства»\n\n"
    "💬 Техподдержка: @support\n"
    "⏱ Среднее время ответа: до 2 часов"
)


# ── Утилиты ──────────────────────────────────────────────────────────────────

async def _safe_edit(callback: CallbackQuery, text: str, **kwargs) -> None:
    """Edit message, silently ignore 'message is not modified' errors."""
    try:
        await callback.message.edit_text(text, **kwargs)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            logger.warning("edit_text failed: %s", e)
    finally:
        await callback.answer()


# ── Команды ──────────────────────────────────────────────────────────────────

@router.message(Command("start", "menu"))
async def cmd_start(message: Message) -> None:
    register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
    )

    first_name = message.from_user.first_name or "друг"
    row = get_active_subscription(message.from_user.id)

    if row and row["subscription_end"]:
        try:
            sub_end = datetime.fromisoformat(row["subscription_end"])
            text = _welcome_text_with_sub(first_name, sub_end)
        except (ValueError, KeyError) as e:
            logger.error(f"error format subscription_end: {e}")
            text = _welcome_text(first_name)
    else:
        text = _welcome_text(first_name)

    await message.answer(text, reply_markup=kb_main())


# ── Навигация ────────────────────────────────────────────────────────────────

@router.callback_query(F.data == "menu_main")
async def cb_main(callback: CallbackQuery) -> None:
    first_name = callback.from_user.first_name or "друг"
    row = get_active_subscription(callback.from_user.id)

    if row and row["subscription_end"]:
        try:
            sub_end = datetime.fromisoformat(row["subscription_end"])
            text = _welcome_text_with_sub(first_name, sub_end)
        except (ValueError, KeyError) as e:
            logger.error(f"error format subscription_end: {e}")
            text = _welcome_text(first_name)
    else:
        text = _welcome_text(first_name)

    await _safe_edit(callback, text, reply_markup=kb_main())


@router.callback_query(F.data == "menu_vpn")
async def cb_vpn(callback: CallbackQuery) -> None:
    await _safe_edit(callback, _VPN_TEXT, reply_markup=kb_vpn_plans())


@router.callback_query(F.data == "menu_tools")
async def cb_tools(callback: CallbackQuery) -> None:
    await _safe_edit(callback, _SOFTWARE_TEXT, reply_markup=kb_tools())

@router.callback_query(F.data == "menu_vpn_clients")
async def cb_vpn_clients(callback: CallbackQuery) -> None:
    await _safe_edit(callback, _SOFTWARE_TEXT, reply_markup=kb_vpn_cliients())

@router.callback_query(F.data == "menu_guides")
async def cb_guides(callback: CallbackQuery) -> None:
    await _safe_edit(callback, _GUIDES_TEXT, reply_markup=kb_guides())


@router.callback_query(F.data == "menu_help")
async def cb_help(callback: CallbackQuery) -> None:
    await _safe_edit(callback, _HELP_TEXT, reply_markup=kb_back_main())
