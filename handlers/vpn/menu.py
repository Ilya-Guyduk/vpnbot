import logging

from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.inline import kb_vpn_plans, kb_tunnel_type
from handlers.utils import safe_edit

from handlers.vpn.payment import router as payment

logger = logging.getLogger(__name__)
router = Router()
router.include_router(payment)

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

_TUNNEL_TYPE_TEXT = (
    "Выберите тип туннеля:"
)

@router.callback_query(F.data == "menu_tunnel_type")
async def cb_vpn(callback: CallbackQuery) -> None:
    await safe_edit(callback, _TUNNEL_TYPE_TEXT, reply_markup=kb_tunnel_type(has_tunnels=True))

@router.callback_query(F.data == "menu_vpn")
async def cb_vpn(callback: CallbackQuery) -> None:
    await safe_edit(callback, _VPN_TEXT, reply_markup=kb_vpn_plans())