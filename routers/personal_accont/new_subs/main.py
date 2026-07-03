import logging
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from services.xui_client.xui_client.client import AuthenticatedClient

from database import db
from routers.utils import safe_edit
from services.cryptobot import create_invoice
from routers.personal_accont.payment_service import PaymentService, create_invoice_message, make_payload, INVOICE_EXPIRY_SECONDS
from config import VPN_PLANS, CRYPTO_ASSET, CRYPTO_BOT_TOKEN, XUI_API_HOST, XUI_SUB_PORT, XUI_SUB_PATH

logger = logging.getLogger(__name__)
router = Router()

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

@router.callback_query(F.data == "new_vpn_sub")
async def cb_vpn(callback: CallbackQuery) -> None:
    """Обработчик кнопки нового туннеля."""
    await safe_edit(callback, _VPN_TEXT, reply_markup=kb_vpn_plans())


def kb_vpn_plans(back_cb: str = "menu_personal_account") -> InlineKeyboardMarkup:
    """Тарифы для нового туннеля."""
    b = InlineKeyboardBuilder()
    for plan_id, plan in VPN_PLANS.items():
        b.button(
            text=f"{plan['name']} — {plan['price']} USDT",
            callback_data=f"buy_vpn_{plan_id}",
        )
    b.button(text="◀️ Назад", callback_data=back_cb)
    b.adjust(1)
    return b.as_markup()

#######################################################################################################

@router.callback_query(F.data.startswith("buy_vpn_"))
async def cb_buy_vpn(callback: CallbackQuery, bot: Bot, xui_client: AuthenticatedClient):
    """Обработчик покупки нового туннеля"""
    if not CRYPTO_BOT_TOKEN:
        await callback.answer("⚠️ Оплата временно недоступна", show_alert=True)
        return
    
    plan_id = callback.data.removeprefix("buy_vpn_")
    if plan_id not in VPN_PLANS:
        await callback.answer("❌ Тариф не найден", show_alert=True)
        return
    
    await callback.answer("⏳ Создаём счёт...")
    
    payment_service = PaymentService(bot, xui_client)
    
    try:
        logger.info(f"Создаём счет на оплату новой подписки: callback.from_user.id:{callback.from_user.id} plan_id:{plan_id}")
        payment_id, preview_end = await payment_service.create_payment(
            tg_id=callback.from_user.id,
            plan_id=plan_id,
            is_extend=False
        )
        
        if not payment_id:
            await callback.message.answer("❌ Не удалось создать платеж")
            return
        
        plan = VPN_PLANS[plan_id]
        invoice = await create_invoice(
            amount=plan["price"],
            asset=CRYPTO_ASSET,
            description=f"{plan['name']} · VPN-подписка",
            payload=make_payload(plan_id, payment_id),
            expires_in=INVOICE_EXPIRY_SECONDS
        )
        
        if not invoice:
            db.mark_payment_failed(payment_id)
            await callback.message.answer(
                "❌ Не удалось создать счёт. Попробуйте позже или обратитесь в @support"
            )
            return
        
        with db.get_db() as conn:
            conn.execute(
                "UPDATE payments SET crypto_invoice_id=? WHERE id=?",
                (invoice.invoice_id, payment_id)
            )
        
        await create_invoice_message(
            callback,
            plan_id,
            plan,
            payment_id,
            preview_end,
            "menu_vpn",
            invoice.pay_url,
            is_extend=False  # <-- явно указываем, что это новый туннель
        )
        
        logger.info(f"Создан инвойс: plan={plan_id} payment={payment_id} invoice={invoice.invoice_id}")
        
    except Exception as e:
        logger.exception("Ошибка при создании инвойса")
        await callback.message.answer("❌ Произошла ошибка. Попробуйте позже.")
