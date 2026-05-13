"""
Обёртка над Crypto Pay API (@CryptoBot).

Документация: https://help.crypt.bot/crypto-pay-api
Тест-бот:     @CryptoTestnetBot
"""

import logging
import aiohttp
from dataclasses import dataclass
from config import CRYPTO_BOT_TOKEN, CRYPTO_BOT_TESTNET

logger = logging.getLogger(__name__)

_BASE = (
    "https://testnet-pay.crypt.bot/api/"
    if CRYPTO_BOT_TESTNET
    else "https://pay.crypt.bot/api/"
)
_HEADERS = {"Crypto-Pay-API-Token": CRYPTO_BOT_TOKEN}


@dataclass
class CryptoInvoice:
    invoice_id: int
    status: str          # active | paid | expired
    pay_url: str         # ссылка для оплаты пользователем
    asset: str
    amount: str
    payload: str         # наш payload для сверки


async def _api(method: str, **params) -> dict | None:
    url = _BASE + method
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=_HEADERS, json=params, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                data = await resp.json()
                if not data.get("ok"):
                    logger.error("CryptoBot API error [%s]: %s", method, data)
                    return None
                return data["result"]
    except Exception as exc:
        logger.exception("CryptoBot request failed [%s]: %s", method, exc)
        return None


async def create_invoice(
    amount: float,
    asset: str,
    description: str,
    payload: str,
    expires_in: int = 3600,
) -> CryptoInvoice | None:
    """Создаёт счёт и возвращает объект CryptoInvoice."""
    result = await _api(
        "createInvoice",
        asset=asset,
        amount=str(amount),
        description=description,
        payload=payload,
        expires_in=expires_in,
        allow_comments=False,
        allow_anonymous=True,
    )
    if not result:
        return None
    return CryptoInvoice(
        invoice_id=result["invoice_id"],
        status=result["status"],
        pay_url=result["bot_invoice_url"],
        asset=result["asset"],
        amount=result["amount"],
        payload=result.get("payload", ""),
    )


async def get_invoices(invoice_ids: list[int]) -> list[CryptoInvoice]:
    """Возвращает список инвойсов по ID."""
    if not invoice_ids:
        return []
    result = await _api(
        "getInvoices",
        invoice_ids=",".join(map(str, invoice_ids)),
    )
    if not result:
        return []
    items = result.get("items", [])
    return [
        CryptoInvoice(
            invoice_id=inv["invoice_id"],
            status=inv["status"],
            pay_url=inv.get("bot_invoice_url", ""),
            asset=inv["asset"],
            amount=inv["amount"],
            payload=inv.get("payload", ""),
        )
        for inv in items
    ]


async def check_app() -> bool:
    """Проверяет корректность токена CryptoBot."""
    result = await _api("getMe")
    if result:
        logger.info("CryptoBot app: %s", result.get("name"))
        return True
    return False
