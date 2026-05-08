from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from config import VPN_PLANS
from data.articles import ARTICLES


def kb_main() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🔒 VPN-сервисы",       callback_data="menu_vpn")
    b.button(text="🛠 Другие инструменты", callback_data="menu_tools")
    b.button(text="📖 Руководства",        callback_data="menu_guides")
    b.button(text="❓ Помощь",             callback_data="menu_help")
    b.adjust(2, 2)
    return b.as_markup()


def kb_vpn_plans() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for plan_id, plan in VPN_PLANS.items():
        b.button(
            text=f"{plan['name']} — ⭐ {plan['price_stars']}",
            callback_data=f"buy_vpn_{plan_id}",
        )
    b.button(text="◀️ Назад", callback_data="menu_main")
    b.adjust(1)
    return b.as_markup()


def kb_tools() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🌐 Tor Browser",    callback_data="tool_tor")
    b.button(text="🔄 Зеркала сайтов", callback_data="tool_mirrors")
    b.button(text="🔧 DNS-настройки",  callback_data="tool_dns")
    b.button(text="🌍 Прокси",         callback_data="tool_proxy")
    b.button(text="◀️ Назад",          callback_data="menu_main")
    b.adjust(2, 2, 1)
    return b.as_markup()


def kb_guides() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="📱 Android",  callback_data="guide_android")
    b.button(text="🍎 iOS",      callback_data="guide_ios")
    b.button(text="💻 Windows",  callback_data="guide_windows")
    b.button(text="🐧 Linux",    callback_data="guide_linux")
    b.button(text="◀️ Назад",    callback_data="menu_main")
    b.adjust(2, 2, 1)
    return b.as_markup()


def kb_back_tools() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="◀️ Назад к инструментам", callback_data="menu_tools")
    return b.as_markup()


def kb_guide(platform: str, article_url: str | None) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if article_url:
        b.button(text="📖 Открыть руководство", url=article_url)
    b.button(text="◀️ Назад к руководствам", callback_data="menu_guides")
    b.adjust(1)
    return b.as_markup()


def kb_back_main() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="◀️ Назад", callback_data="menu_main")
    return b.as_markup()
