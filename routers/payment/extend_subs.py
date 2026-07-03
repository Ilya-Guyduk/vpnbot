import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery
from database import db

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from config import VPN_PLANS, CRYPTO_ASSET, CRYPTO_BOT_TOKEN
from services.cryptobot import create_invoice
from routers.personal_accont.payment_service import PaymentService, create_invoice_message, make_payload, INVOICE_EXPIRY_SECONDS
from services.xui_client.xui_client.client import AuthenticatedClient


logger = logging.getLogger(__name__)
router = Router()


@router.callback_query(F.data.startswith("extend_subs_"))
async def cb_ext_vpn(callback: CallbackQuery, bot: Bot, xui_client: AuthenticatedClient):
    logger.debug(f"cb_ext_vpn callback:{callback}")
    """Обработчик продления существующего туннеля"""
    if not CRYPTO_BOT_TOKEN:
        await callback.answer("⚠️ Оплата временно недоступна", show_alert=True)
        return
    
    parts = callback.data.removeprefix("extend_subs_").rsplit("__", 1)
    if len(parts) != 2:
        logger.error(f"Неверный формат parts:{parts}")
        await callback.answer("❌ Неверный формат", show_alert=True)
        return
    
    plan_id, user_id_str = parts
    if plan_id not in VPN_PLANS:
        logger.error(f"Тариф не найден plan_id:{plan_id}")
        await callback.answer("❌ Тариф не найден", show_alert=True)
        return
    
    try:
        user_id = str(user_id_str)
    except ValueError:
        logger.error(f"Неверный ID пользователя user_id_str:{user_id_str}")
        await callback.answer("❌ Неверный ID пользователя", show_alert=True)
        return
    
    await callback.answer("⏳ Создаём счёт...")
    
    payment_service = PaymentService(bot, xui_client)
    
    try:
        payment_id, preview_end = await payment_service.create_payment(
            callback.from_user.id,
            plan_id,
            is_extend=True,
        )
        
        if not payment_id:
            await callback.message.answer("❌ Не удалось создать платеж")
            return
        
        plan = VPN_PLANS[plan_id]
        invoice = await create_invoice(
            amount=plan["price"],
            asset=CRYPTO_ASSET,
            description=f"{plan['name']} · Продление VPN",
            payload=make_payload(plan_id, payment_id),
            expires_in=INVOICE_EXPIRY_SECONDS
        )
        
        if not invoice:
            db.mark_payment_failed(payment_id)
            await callback.message.answer(
                "❌ Не удалось создать счёт. Попробуйте позже"
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
            "menu_extend_vpn",
            invoice.pay_url,
            is_extend=True  # <-- явно указываем, что это продление
        )
        
        logger.info(f"Создан инвойс на продление: plan={plan_id} payment={payment_id}")
        
    except Exception as e:
        logger.exception("Ошибка при создании инвойса на продление")
        await callback.message.answer("❌ Произошла ошибка. Попробуйте позже.")

