from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from config import VPN_PLANS
from data.articles import ARTICLES
from data.vpn_clients import VPN_CLIENTS, ICONS
from config import SOFTWARE_MENU_ENABLED, VPN_MENU_ENABLED, GUIDES_MENU_ENABLED, SETTINGS_MENU_ENABLED, LINKS_MENU_ENABLED, BOTS_MENU_ENABLED, MIRRORS_MENU_ENABLED, HELP_MENU_ENABLED


def kb_main() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    if VPN_MENU_ENABLED:
        b.button(text="🔒 Black List VPN",      callback_data="menu_tunnel_type")
    if SOFTWARE_MENU_ENABLED:
        b.button(text="🛠 Софт",                 callback_data="menu_software")
    if GUIDES_MENU_ENABLED:
        b.button(text="📖 Руководства",         callback_data="menu_guides")
    if SETTINGS_MENU_ENABLED:
        b.button(text="🛠 Настройки ПО",         callback_data="menu_settings")
    if LINKS_MENU_ENABLED:
        b.button(text="🛠 Полезные ссылки",      callback_data="menu_links")
    if BOTS_MENU_ENABLED:
        b.button(text="📖 Другие боты",         callback_data="menu_bots")
    if MIRRORS_MENU_ENABLED:
        b.button(text="🔄 Зеркала сайтов",      callback_data="tool_mirrors")
    if HELP_MENU_ENABLED:
        b.button(text="❓ Помощь",              callback_data="menu_help")
    b.adjust(1, 2, 2)
    return b.as_markup()

def kb_tunnel_type() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🌍 Новый туннель",    callback_data="menu_vpn")
    b.button(text="🌍 Существующий",    callback_data="menu_vpn")
    b.button(text="◀️ Назад", callback_data="menu_main")
    return b.as_markup()


def kb_vpn_plans() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for plan_id, plan in VPN_PLANS.items():
        b.button(
            text=f"{plan['name']} — ⭐ {plan['price']}",
            callback_data=f"buy_vpn_{plan_id}",
        )
    b.button(text="◀️ Назад", callback_data="menu_main")
    b.adjust(1)
    return b.as_markup()


def kb_software() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🌍 VPN-клиенты",    callback_data="menu_vpn_clients")
    b.button(text="🌍 VPN-серверы",    callback_data="tool_proxy")
    b.button(text="🌐 Tor Browser",    callback_data="tool_tor")
    b.button(text="🌍 Прокси",         callback_data="tool_proxy")
    b.button(text="◀️ Назад",          callback_data="menu_main")
    b.adjust(2, 2, 1)
    return b.as_markup()


def kb_vpn_clients() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()

    for client_id, client in VPN_CLIENTS.items():
        icons = "".join(ICONS[p] for p in client["platforms"])

        b.button(
            text=f"{icons} {client['name']}",
            callback_data=f"vpn_client:{client_id}"
        )

    b.button(
        text="◀️ Назад",
        callback_data="menu_software"
    )

    b.adjust(1)
    return b.as_markup()

def kb_vpn_client_platforms(client_id: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()

    client = VPN_CLIENTS[client_id]

    for platform in client["platforms"]:
        version = client["versions"].get(platform)

        if version:
            b.button(
                text=f"{ICONS[platform]} {platform.capitalize()}",
                callback_data=f"vpn_platform:{client_id}:{platform}"
            )

    b.button(
        text="◀️ Назад",
        callback_data="menu_vpn_clients"
    )

    b.adjust(2)
    return b.as_markup()

def kb_vpn_client_versions(
    client_id: str,
    platform: str
) -> InlineKeyboardMarkup:

    b = InlineKeyboardBuilder()

    client = VPN_CLIENTS[client_id]
    version = client["versions"][platform]

    b.button(
        text="⬇️ Скачать",
        url=version["url"]
    )

    b.button(
        text="◀️ Назад",
        callback_data=f"vpn_client:{client_id}"
    )

    b.adjust(1)

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
