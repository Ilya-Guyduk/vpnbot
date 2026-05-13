"""Главное меню и навигация."""

import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.db import register_user, get_active_subscription
from keyboards.inline import kb_main, kb_vpn_plans, kb_guides, kb_back_main

logger = logging.getLogger(__name__)
router = Router()


# ── Тексты ───────────────────────────────────────────────────────────────────

def _welcome_text(first_name: str) -> str:
    return (
        f"👤 <b>{first_name}.</b>\n\n"
        "Связь установлена. Добро пожаловать в <b>Black List</b>.\n\n"
        "Министерство правды контролирует то, что ты видишь.\n"
        "Мы контролируем то, что они не хотят, чтобы ты видел.\n\n"
        "——————————————————\n"
        "  🔒 <b>Black List VPN</b> — туннель сквозь Стену\n"
        "  📦 <b>Арсенал</b> — софт, который они хотят запретить\n"
        "  ⚙️ <b>DNS</b> — обойти блокировку за 5 минут\n"
        "  🌍 <b>Прокси</b> — анонимность без следов\n"
        "  📖 <b>Инструкции</b> — пошагово для любой платформы\n"
        "——————————————————\n\n"
        "Выбери раздел. Время работает против нас."
    )


def _welcome_text_with_sub(first_name: str, sub_end: datetime) -> str:
    days_left = (sub_end - datetime.now()).days
    if days_left > 7:
        status = f"🟢 Активен · осталось <b>{days_left} дн.</b>"
    elif days_left > 0:
        status = f"🟡 Истекает через <b>{days_left} дн.</b> — продли до отключения"
    else:
        status = "🔴 Истёк — ты снова за Стеной"

    return (
        f"👤 <b>{first_name}.</b> Связь восстановлена.\n\n"
        f"📡 <b>Статус туннеля:</b> {status}\n\n"
        "——————————————————\n"
        "Выбери раздел:"
    )


_VPN_TEXT = (
    "🔒 <b>Black List VPN</b>\n\n"
    "Они называют это «регулированием».\n"
    "Мы называем это тем, чем это является.\n\n"
    "Выбери тариф — после оплаты сервер поднимется автоматически. "
    "Никаких анкет, никаких имён.\n\n"
    "⚡ Активация: <b>~60 секунд</b>\n"
    "🌍 Серверы вне юрисдикции РКН\n"
    "🔑 Один ключ — все устройства\n"
    "👁 Логи не ведутся"
)

_GUIDES_TEXT = (
    "📖 <b>Инструкции</b>\n\n"
    "Знание — оружие. Здесь оно бесплатно.\n\n"
    "Пошаговые руководства со скриншотами.\n"
    "Выбери платформу:"
)

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


# ── Утилиты ──────────────────────────────────────────────────────────────────

async def _safe_edit(callback: CallbackQuery, text: str, **kwargs) -> None:
    try:
        await callback.message.edit_text(text, **kwargs)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            logger.warning("edit_text failed: %s", e)
    finally:
        await callback.answer()


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
    await _safe_edit(callback, text, reply_markup=kb_main())


@router.callback_query(F.data == "menu_vpn")
async def cb_vpn(callback: CallbackQuery) -> None:
    await _safe_edit(callback, _VPN_TEXT, reply_markup=kb_vpn_plans())


@router.callback_query(F.data == "menu_guides")
async def cb_guides(callback: CallbackQuery) -> None:
    await _safe_edit(callback, _GUIDES_TEXT, reply_markup=kb_guides())


@router.callback_query(F.data == "menu_help")
async def cb_help(callback: CallbackQuery) -> None:
    await _safe_edit(callback, _HELP_TEXT, reply_markup=kb_back_main())
