import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup
from config import VPN_PLANS

from routers.payment.extend_subs import router as extend_subs_router
from routers.payment.new_subs import router as new_subs_router


logger = logging.getLogger(__name__)
router = Router()
router.include_router(extend_subs_router)
router.include_router(new_subs_router)


@router.callback_query(F.data.startswith("pay_type_subs_"))
async def cb_pay_type_subs(callback: CallbackQuery):
    """Обработчик выбора туннеля для продления"""
    logger.debug(f"cb_pay_type_subs callback:{callback}")
    logger.info(f"cb_pay_type_subs callback.data:{callback.data}")

    subs_name = callback.data.removeprefix("pay_type_subs_")
    
    await callback.message.edit_text(
        f"♻️ <b>Оплата</b>\n\n"

        "Выбери способ оплаты:",
        reply_markup=kb_pay_type(subs_name)
    )
    await callback.answer()


def kb_pay_type(subs_name: str) -> InlineKeyboardMarkup:
    """Тарифы для продления конкретного туннеля."""
    b = InlineKeyboardBuilder()
    b.button(text=f"CryptoPay", callback_data=f"subs_plans_{subs_name}")
    b.button(text="◀️ Назад", callback_data=f"pay_type_subs_{subs_name}")
    b.adjust(1)
    return b.as_markup()


@router.callback_query(F.data.startswith("subs_plans_"))
async def cb_subs_plans(callback: CallbackQuery):
    """Обработчик выбора плана"""
    logger.debug(f"cb_subs_plans callback:{callback}")
    logger.debug(f"cb_subs_plans callback.data:{callback.data}")
    subs_name = callback.data.removeprefix("subs_plans_")
    
    await callback.message.edit_text(
        f"♻️ <b>Доступные планы</b>\n\n"

        "Выбери доступные планы:",
        reply_markup=kb_subs_plans(subs_name)
    )
    await callback.answer()


def kb_subs_plans(subs_name: str) -> InlineKeyboardMarkup:
    """Тарифы для туннеля."""
    b = InlineKeyboardBuilder()
    for plan_id, plan in VPN_PLANS.items():
        if subs_name != "":
            b.button(
                text=f"{plan['name']} — {plan['price']} USDT",
                callback_data=f"extend_subs_{plan_id}__{subs_name}",
            )
        else:
            b.button(
                text=f"{plan['name']} — {plan['price']} USDT",
                callback_data=f"new_subs_{plan_id}",
            )
    b.button(text="◀️ Назад", callback_data=f"extend_subs_{subs_name}")
    b.adjust(1)
    return b.as_markup()





