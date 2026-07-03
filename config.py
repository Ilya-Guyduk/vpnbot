import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

USE_SOCKS5: bool = os.getenv("USE_SOCKS5", "false").lower() == "true"


# ── Бот ──────────────────────────────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env!")

ADMIN_IDS: list[int] = [
    int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
]
if not ADMIN_IDS:
    logger.warning("ADMIN_IDS не задан — админ-команды недоступны")

# ── CryptoBot ────────────────────────────────────────────────────────────────
CRYPTO_BOT_TOKEN: str = os.getenv("CRYPTO_BOT_TOKEN", "")
if not CRYPTO_BOT_TOKEN:
    logger.warning("CRYPTO_BOT_TOKEN не задан — оплата недоступна")

CRYPTO_BOT_TESTNET: bool = os.getenv("CRYPTO_BOT_TESTNET", "false").lower() == "true"
CRYPTO_ASSET: str = os.getenv("CRYPTO_ASSET", "USDT")

# ── GitHub ───────────────────────────────────────────────────────────────────
# Опционально: увеличивает лимит GitHub API с 60 до 5000 запросов в час
# Создать: github.com/settings/tokens → Generate new token (classic) → без скоупов
GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")

# -- XUI-API
XUI_API_HOST: str = os.getenv("XUI_API_HOST", "")
XUI_API_PORT: str = os.getenv("XUI_API_PORT", "")
XUI_API_PATH: str = os.getenv("XUI_API_PATH", "")
XUI_SUB_PORT: str = os.getenv("XUI_SUB_PORT", "")
XUI_SUB_PATH: str = os.getenv("XUI_SUB_PATH", "")

XUI_API_USERNAME: str = os.getenv("XUI_API_USERNAME", "")
XUI_API_PASSWORD: str = os.getenv("XUI_API_PASSWORD", "")
XUI_API_TOKEN: str = os.getenv("XUI_API_TOKEN", "")




# ── Ansible ───────────────────────────────────────────────────────────────────
ANSIBLE_PLAYBOOK_PATH: str = os.getenv("ANSIBLE_PLAYBOOK_PATH", "ansible/playbooks/create_vpn_user.yml")
ANSIBLE_INVENTORY: str    = os.getenv("ANSIBLE_INVENTORY", "ansible/inventory/inventory.yml")
VPN_CONFIG_OUTPUT_DIR: str = os.getenv("VPN_CONFIG_OUTPUT_DIR", "/tmp/vpn_configs")
ANSIBLE_TIMEOUT: int       = int(os.getenv("ANSIBLE_TIMEOUT", "120"))

# ── Тарифы (цены в USDT) ─────────────────────────────────────────────────────
VPN_PLANS: dict[str, dict] = {
    "basic_1m":   {"name": "Базовый · 1 месяц",   "price": 3.0,  "duration": 30},
    "premium_3m": {"name": "Премиум · 3 месяца",  "price": 12.0, "duration": 90},
    "premium_1y": {"name": "Премиум · 1 год",     "price": 35.0, "duration": 365},
}


# Фича-флаги 

MAIN_MENU_ENABLED: bool = os.getenv("MAIN_MENU_ENABLED", "false").lower() == "true"
ADMIN_MENU_ENABLED: bool = os.getenv("ADMIN_MENU_ENABLED", "false").lower() == "true"
INLINE_MODE_ENABLED: bool = os.getenv("INLINE_MODE_ENABLED", "false").lower() == "true"

SOFTWARE_MENU_ENABLED: bool = os.getenv("SOFTWARE_MENU_ENABLED", "false").lower() == "true"
VPN_MENU_ENABLED: bool = os.getenv("VPN_MENU_ENABLED", "false").lower() == "true"
GUIDES_MENU_ENABLED: bool = os.getenv("GUIDES_MENU_ENABLED", "false").lower() == "true"
SETTINGS_MENU_ENABLED: bool = os.getenv("SETTINGS_MENU_ENABLED", "false").lower() == "true"
LINKS_MENU_ENABLED: bool = os.getenv("LINKS_MENU_ENABLED", "false").lower() == "true"
BOTS_MENU_ENABLED: bool = os.getenv("BOTS_MENU_ENABLED", "false").lower() == "true"
MIRRORS_MENU_ENABLED: bool = os.getenv("MIRRORS_MENU_ENABLED", "false").lower() == "true"

HELP_MENU_ENABLED: bool = os.getenv("HELP_MENU_ENABLED", "false").lower() == "true"