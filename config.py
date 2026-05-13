import os
import logging
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

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

# ── Ansible ───────────────────────────────────────────────────────────────────
ANSIBLE_PLAYBOOK_PATH: str = os.getenv("ANSIBLE_PLAYBOOK_PATH", "playbooks/create_vpn_user.yml")
ANSIBLE_INVENTORY: str    = os.getenv("ANSIBLE_INVENTORY", "inventory/hosts.ini")
VPN_CONFIG_OUTPUT_DIR: str = os.getenv("VPN_CONFIG_OUTPUT_DIR", "/tmp/vpn_configs")
ANSIBLE_TIMEOUT: int       = int(os.getenv("ANSIBLE_TIMEOUT", "120"))

# ── Тарифы (цены в USDT) ─────────────────────────────────────────────────────
VPN_PLANS: dict[str, dict] = {
    "basic_1m":   {"name": "Базовый · 1 месяц",   "price": 3.0,  "duration": 30},
    "premium_1m": {"name": "Премиум · 1 месяц",   "price": 5.0,  "duration": 30},
    "premium_3m": {"name": "Премиум · 3 месяца",  "price": 12.0, "duration": 90},
    "premium_1y": {"name": "Премиум · 1 год",     "price": 35.0, "duration": 365},
}
