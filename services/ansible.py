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

from config import ANSIBLE_PLAYBOOK_PATH, ANSIBLE_INVENTORY, VPN_CONFIG_OUTPUT_DIR, ANSIBLE_TIMEOUT

logger = logging.getLogger(__name__)


async def provision_vpn_user(user_id: int, duration_days: int) -> str | None:
    """
    Запускает Ansible-плейбук и возвращает строку VPN-конфига.
    Возвращает None, если провижининг завершился ошибкой.
    """
    output_dir = Path(VPN_CONFIG_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    config_path = output_dir / f"user_{user_id}.conf"

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
