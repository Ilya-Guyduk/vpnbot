"""
Сервис запуска Ansible-роли для провижининга VPN-пользователя.

Ожидаемое поведение роли:
  - Принимает extra-vars: user_id, duration_days, config_output_path
  - Создаёт пользователя на VPN-сервере
  - Записывает готовый конфиг (строку подключения) в config_output_path
"""

import asyncio
import logging
from pathlib import Path
from aiogram import Bot

from database import db
from services.cryptobot import get_invoices
from handlers.vpn.payment import _deliver_vpn
from config import ANSIBLE_PLAYBOOK_PATH, ANSIBLE_INVENTORY, VPN_CONFIG_OUTPUT_DIR, ANSIBLE_TIMEOUT

logger = logging.getLogger(__name__)

POLL_INTERVAL = 30  # секунд

async def provision_vpn_user(user_id: int, duration_days: int) -> str | None:
    """
    Запускает Ansible-плейбук и возвращает строку VPN-конфига.
    Возвращает None, если провижининг завершился ошибкой.
    """
    output_dir = Path(VPN_CONFIG_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = output_dir / f"user_{user_id}.conf"

    logging.info(f"output_dir: {output_dir}, config_path: {config_path}")
    # Удаляем старый файл, чтобы не вернуть устаревший конфиг
    if config_path.exists():
        config_path.unlink()

    extra_vars = (
        f"user_id={user_id} "
        f"duration_days={duration_days} "
        f"config_output_path={config_path}"
    )

    cmd = [
        "ansible-playbook",
        ANSIBLE_PLAYBOOK_PATH,
        "-i", ANSIBLE_INVENTORY,
        "--extra-vars", extra_vars,
    ]

    logger.info("Запуск Ansible для user_id=%s: %s", user_id, " ".join(cmd))

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            process.communicate(), timeout=ANSIBLE_TIMEOUT
        )

        if process.returncode != 0:
            logger.error(
                "Ansible вернул код %s\nSTDOUT: %s\nSTDERR: %s",
                process.returncode,
                stdout.decode(errors="replace"),
                stderr.decode(errors="replace"),
            )
            return None

        if not config_path.exists():
            logger.error("Ansible завершился успешно, но файл конфига не создан: %s", config_path)
            return None

        config = config_path.read_text(encoding="utf-8").strip()
        config_path.unlink(missing_ok=True)   # убираем временный файл
        logger.info("VPN-конфиг для user_id=%s успешно получен", user_id)
        return config

    except asyncio.TimeoutError:
        logger.error("Ansible превысил таймаут (%s с) для user_id=%s", ANSIBLE_TIMEOUT, user_id)
        try:
            process.kill()
        except Exception:
            pass
        return None
    except FileNotFoundError:
        logger.error("ansible-playbook не найден — убедитесь, что Ansible установлен")
        return None
    except Exception as exc:
        logger.exception("Неожиданная ошибка при запуске Ansible: %s", exc)
        return None



async def ansi_scheduler():
    logger.info("Поллер Ansible тасок запущен (интервал %ds)", POLL_INTERVAL)
    while True:
        try:
            await _poll_once(bot)
        except Exception as exc:
            logger.exception("Ошибка в поллере: %s", exc)
        await asyncio.sleep(POLL_INTERVAL)

async def _poll_once(bot: Bot) -> None:
    pending = db.get_pending_crypto_orders()
    if not pending:
        return

    invoice_ids = [row["crypto_invoice_id"] for row in pending]
    logger.debug("Проверяем %d pending-заказов: %s", len(invoice_ids), invoice_ids)

    invoices = await get_invoices(invoice_ids)
    inv_map = {inv.invoice_id: inv for inv in invoices}

    # Чистим просроченные заказы
    expired_count = db.expire_old_pending_orders(older_than_hours=2)
    if expired_count:
        logger.info("Помечено как expired: %d заказов", expired_count)

    for row in pending:
        inv = inv_map.get(row["crypto_invoice_id"])
        if not inv:
            continue

        if inv.status == "paid":
            logger.info(
                "Оплата найдена поллером: order_id=%s invoice_id=%s",
                row["id"], inv.invoice_id,
            )
            await _deliver_vpn(bot, row["user_id"], row["id"], row, inv)

        elif inv.status == "expired":
            db.fail_order(row["id"])
            logger.info("Invoice %s истёк, order %s → expired", inv.invoice_id, row["id"])