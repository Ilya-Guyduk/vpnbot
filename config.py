import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ── Бот ──────────────────────────────────────────────────────────────────────
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env файле!")

ADMIN_IDS: list[int] = [
    int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()
]
if not ADMIN_IDS:
    logger.warning("ADMIN_IDS не задан — админ-команды будут недоступны")

# ── Ansible ───────────────────────────────────────────────────────────────────
ANSIBLE_PLAYBOOK_PATH: str = os.getenv(
    "ANSIBLE_PLAYBOOK_PATH", "playbooks/create_vpn_user.yml"
)
ANSIBLE_INVENTORY: str = os.getenv("ANSIBLE_INVENTORY", "inventory/hosts.ini")
VPN_CONFIG_OUTPUT_DIR: str = os.getenv("VPN_CONFIG_OUTPUT_DIR", "/tmp/vpn_configs")
ANSIBLE_TIMEOUT: int = int(os.getenv("ANSIBLE_TIMEOUT", "120"))

# ── Тарифы (цены в Telegram Stars) ───────────────────────────────────────────
# 1 Star ≈ 0.013 USD; ориентировочный курс на момент написания
VPN_PLANS: dict[str, dict] = {
    "basic_1m":   {"name": "Базовый · 1 месяц",   "price_stars": 150,  "duration": 30},
    "premium_1m": {"name": "Премиум · 1 месяц",   "price_stars": 250,  "duration": 30},
    "premium_3m": {"name": "Премиум · 3 месяца",  "price_stars": 600,  "duration": 90},
    "premium_1y": {"name": "Премиум · 1 год",     "price_stars": 1750, "duration": 365},
}
