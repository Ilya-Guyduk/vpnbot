"""Главное меню и навигация."""

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from database.db import register_user
from keyboards.inline import kb_main, kb_vpn_plans, kb_tools, kb_guides

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    register_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
    )
    await message.answer(
        "🛡 <b>Бот для доступа к свободному интернету</b>\n\n"
        "Здесь вы найдёте инструменты для обхода цензуры и сохранения приватности:\n\n"
        "• Надёжные VPN-сервисы\n"
        "• Актуальные зеркала сайтов\n"
        "• Tor Browser и прокси\n"
        "• Подробные руководства\n\n"
        "Выберите интересующий раздел:",
        reply_markup=kb_main(),
    )


@router.callback_query(F.data == "menu_main")
async def cb_main(callback: CallbackQuery) -> None:
    await callback.message.edit_text("🛡 Выберите раздел:", reply_markup=kb_main())
    await callback.answer()


@router.callback_query(F.data == "menu_vpn")
async def cb_vpn(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🔒 <b>VPN-сервисы</b>\n\n"
        "Выберите тариф. После оплаты Telegram Stars бот автоматически "
        "подготовит и пришлёт вам ключ подключения.\n\n"
        "<i>Все серверы находятся в юрисдикциях с уважением к приватности.</i>",
        reply_markup=kb_vpn_plans(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_tools")
async def cb_tools(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "🛠 <b>Другие инструменты обхода цензуры:</b>",
        reply_markup=kb_tools(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_guides")
async def cb_guides(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "📖 <b>Руководства по настройке:</b>\nВыберите вашу платформу:",
        reply_markup=kb_guides(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_help")
async def cb_help(callback: CallbackQuery) -> None:
    from keyboards.inline import kb_back_main
    await callback.message.edit_text(
        "❓ <b>Помощь</b>\n\n"
        "1. Выберите инструмент из меню\n"
        "2. Для VPN — выберите тариф и оплатите Telegram Stars\n"
        "3. Бот автоматически выдаст ключ подключения\n"
        "4. Следуйте инструкциям в разделе «Руководства»\n\n"
        "По техническим вопросам: @support",
        reply_markup=kb_back_main(),
    )
    await callback.answer()
