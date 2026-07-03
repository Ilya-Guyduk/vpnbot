import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from database import db

from config import VPN_PLANS, CRYPTO_ASSET, CRYPTO_BOT_TOKEN
from services.cryptobot import create_invoice
from services.xui_client.xui_client.client import AuthenticatedClient

from routers.personal_accont.payment_service import PaymentService, create_invoice_message, make_payload, INVOICE_EXPIRY_SECONDS


logger = logging.getLogger(__name__)
router = Router()



@router.callback_query(F.data.startswith("new_subs_"))
async def cb_buy_vpn(callback: CallbackQuery, bot: Bot, xui_client: AuthenticatedClient):
    """Обработчик покупки нового туннеля"""
    if not CRYPTO_BOT_TOKEN:
        await callback.answer("⚠️ Оплата временно недоступна", show_alert=True)
        return
    
    plan_id = callback.data.removeprefix("new_subs_")
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
