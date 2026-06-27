"""
Оплата через CryptoBot.

Два сценария:
  Новый туннель:      buy_vpn_{plan_id}       → sub_end = MAX(активных) + days
  Продление туннеля:  ext_vpn_{plan_id}_{tid} → sub_end = tunnel.sub_end + days
"""

import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import VPN_PLANS, ADMIN_IDS, CRYPTO_ASSET, CRYPTO_BOT_TOKEN
from database import db
from keyboards.inline import kb_main, kb_vpn_plans_extend
from services.cryptobot import create_invoice, get_invoices
from services.xui_panel_api_client.xui_panel_api_client.models.client import Client

from services.xui_panel_api_client.xui_panel_api_client.client import AuthenticatedClient
from services.xui_panel_api_client.xui_panel_api_client.api.clients.get_panel_api_clients_get_email import (
    asyncio as get_client,
)
from services.xui_panel_api_client.xui_panel_api_client.api.clients.post_panel_api_clients_add import (
    asyncio as create_client,
)
from services.xui_panel_api_client.xui_panel_api_client.api.clients.post_panel_api_clients_update_email import (
    asyncio as update_client,
)

logger = logging.getLogger(__name__)
router = Router()

# Константы
SEP = "|"
INVOICE_EXPIRY_SECONDS = 3600


@dataclass
class TunnelInfo:
    """Информация о туннеле из 3x-ui"""
    client_id: str
    email: str
    group: str
    expiry_time: Optional[datetime]
    is_active: bool
    comment: str
    limit_ip: int
    reset: int
    security: str
    sub_id: str
    tg_id: str
    total_gb: int

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'TunnelInfo':
        """Создает объект из ответа API 3x-ui"""
        expiry_ms = data.get("expiryTime", 0)
        expiry_time = datetime.fromtimestamp(expiry_ms / 1000) if expiry_ms > 0 else None
        
        return cls(
            client_id=data.get("id", ""),
            email=data.get("email", ""),
            group=data.get("group", "-"),
            expiry_time=expiry_time,
            is_active=data.get("enable", False),
            comment=data.get("comment", ""),
            limit_ip=data.get("limit_ip", ""),
            reset=data.get("reset", ""),
            security=data.get("security", ""),
            sub_id=data.get("sub_id", ""),
            tg_id=data.get("tg_id", ""),
            total_gb=data.get("total_gb", ""),
        )


class PaymentService:
    """Сервис для работы с платежами"""
    
    def __init__(self, bot: Bot, xui_client: AuthenticatedClient):
        self.bot = bot
        self.xui_client = xui_client
    
    async def create_payment(
        self, 
        user_id: int, 
        plan_id: str,
    ) -> Tuple[Optional[int], Optional[datetime]]:
        """
        Создает платеж в БД
        Возвращает (payment_id, new_sub_end)
        """
        plan = VPN_PLANS[plan_id]
        
        # Рассчитываем дату окончания
        new_sub_end = await self._calculate_new_sub_end(user_id, plan["duration"])
        
        # Создаем платеж в БД
        payment_id = db.create_payment(
            user_id=user_id,
            duration_days=plan["duration"],
            amount_rub=plan.get("price_rub", 0),
            amount_crypto=str(plan["price"]),
            crypto_asset=CRYPTO_ASSET,
            crypto_invoice_id=0  # Временно, обновим после создания инвойса
        )
        
        return payment_id, new_sub_end
    
    async def process_payment(
        self, 
        payment_id: int, 
        invoice_id: int,
        user_id: int,
        plan_id: str,
        duration_days: int,
        expires_at: datetime,
    ) -> bool:
        """
        Обрабатывает успешную оплату: создает/обновляет туннель в 3x-ui
        """
        try:
            plan = VPN_PLANS[plan_id]
            
            # Получаем существующий туннель или создаем новый
            tunnel_info = await self._get_tunnel_info(str(user_id))
            
            if tunnel_info and tunnel_info.is_active:
                # Обновляем существующий туннель
                # Проверяем, нужно ли продлить
                if tunnel_info.expiry_time and tunnel_info.expiry_time > datetime.now():
                    new_expiry = tunnel_info.expiry_time + timedelta(days=duration_days)
                else:
                    new_expiry = datetime.now() + timedelta(days=duration_days)
                    
                await self._update_tunnel(str(user_id), new_expiry)
            else:
                # Создаем новый туннель
                new_expiry = datetime.now() + timedelta(days=duration_days)
                await self._create_new_tunnel(str(user_id), new_expiry)
            
            # Отмечаем платеж как оплаченный
            db.mark_payment_paid(payment_id, new_expiry)
            
            # Уведомляем пользователя
            await self._notify_user(user_id, new_expiry)
            
            # Уведомляем админов
            await self._notify_admins(user_id, plan, payment_id, invoice_id, new_expiry)
            
            return True
            
        except Exception as e:
            logger.exception(f"Ошибка при обработке оплаты payment_id={payment_id}")
            db.mark_payment_failed(payment_id)
            return False
    
    async def _calculate_new_sub_end(self, user_id: int, add_days: int) -> datetime:
        """
        Рассчитывает новую дату окончания подписки
        
        Аргументы:
            user_id: ID пользователя
            add_days: количество дней для добавления
        
        Возвращает:
            Новая дата окончания
        """
        now = datetime.now()
        
        # Получаем все активные подписки пользователя
        active_subscriptions = db.get_active_subscriptions(user_id)
        
        if active_subscriptions:
            # Находим максимальную дату окончания
            latest_end = max(
                datetime.fromisoformat(sub["expires_at"]) 
                for sub in active_subscriptions
                if sub["expires_at"] is not None
            )
            
            if latest_end > now:
                new_end = latest_end + timedelta(days=add_days)
                logger.info("Новая подписка продолжает MAX %s → %s (+%d дн.)",
                        latest_end.strftime("%d.%m.%Y"),
                        new_end.strftime("%d.%m.%Y"),
                        add_days)
                return new_end
        
        # Иначе стартуем с today
        new_end = now + timedelta(days=add_days)
        logger.info("Новая подписка до %s (%d дн.)",
                new_end.strftime("%d.%m.%Y"), 
                add_days)
        return new_end
    
    async def _get_tunnel_info(self, email: str) -> Optional[TunnelInfo]:
        """Получает информацию о туннеле из 3x-ui"""
        try:
            result = await get_client(
                email=email,
                client=self.xui_client
            )
            
            if result and result.success and result.obj:
                return TunnelInfo.from_api_response(result.obj["client"])
        except Exception as e:
            logger.warning(f"Не удалось получить туннель для {email}: {e}")
        
        return None
    
    async def _update_tunnel(self, email: str, new_expiry: datetime):
        """Обновляет существующий туннель"""
        try:
            # Создаем объект Client с обновленными данными
            current_tunnel = await self._get_tunnel_info(email)
            
            if current_tunnel:
                client_data = Client(
                    comment=current_tunnel.comment,
                    limit_ip=current_tunnel.limit_ip,
                    reset=current_tunnel.reset,
                    security=current_tunnel.security,
                    sub_id=current_tunnel.sub_id,
                    tg_id=current_tunnel.tg_id,
                    total_gb=current_tunnel.total_gb,
                    id=current_tunnel.client_id,
                    email=email,
                    expiry_time=int(new_expiry.timestamp() * 1000),
                    enable=True,
                    group=current_tunnel.group,
                )
                
                await update_client(
                    email=email,
                    client=self.xui_client,
                    body=client_data
                )
                logger.info(f"Обновлен туннель {email} до {new_expiry.strftime('%d.%m.%Y')}")
            else:
                logger.warning(f"Туннель {email} не найден для обновления")
                
        except Exception as e:
            logger.error(f"Ошибка при обновлении туннеля {email}: {e}")
            raise

    async def _create_new_tunnel(self, email: str, new_expiry: datetime):
        """Создает новый туннель"""
        try:
            client_data = Client(
                email=email,
                expiry_time=int(new_expiry.timestamp() * 1000),
                enable=True,
                limit_ip=0,
                total_gb=0,
                group="vpn_users",
                security="auto",
            )
            
            await create_client(
                email=email,
                client=self.xui_client,
                body=client_data
            )
            logger.info(f"Создан новый туннель для {email} до {new_expiry.strftime('%d.%m.%Y')}")
            
        except Exception as e:
            logger.error(f"Ошибка при создании туннеля {email}: {e}")
            raise
    
    async def _notify_user(self, user_id: int, expiry_date: datetime):
        """Уведомляет пользователя об активации"""
        await self.bot.send_message(
            user_id,
            "✅ <b>Туннель активирован.</b>\n\n"
            f"📅 <b>Активен до:</b> {expiry_date.strftime('%d.%m.%Y')}\n\n"
            "📖 Как подключиться — раздел «Руководства».",
            reply_markup=kb_main()
        )
    
    async def _notify_admins(
        self, 
        user_id: int, 
        plan: dict, 
        payment_id: int,
        invoice_id: int,
        new_sub_end: datetime
    ):
        """Уведомляет админов о продаже"""
        text = (
            f"💰 Новая продажа (CryptoBot)\n"
            f"User: {user_id} | Тариф: {plan['name']}\n"
            f"Сумма: {plan['price']} {CRYPTO_ASSET}\n"
            f"Активен до: {new_sub_end.strftime('%d.%m.%Y')}\n"
            f"Payment: {payment_id} | Invoice: {invoice_id}"
        )
        
        for admin_id in ADMIN_IDS:
            try:
                await self.bot.send_message(admin_id, text)
            except Exception as e:
                logger.warning(f"Не удалось уведомить админа {admin_id}: {e}")


def make_payload(plan_id: str, payment_id: int) -> str:
    """Создает payload для CryptoBot инвойса"""
    return f"vpn{SEP}{plan_id}{SEP}{payment_id}"


def parse_payload(payload: str) -> Tuple[str, int]:
    """Парсит payload из CryptoBot инвойса"""
    parts = payload.split(SEP)
    if len(parts) != 3 or parts[0] != "vpn":
        raise ValueError("Invalid payload format")
    return parts[1], int(parts[2])


async def create_invoice_message(
    callback: CallbackQuery,
    plan_id: str,
    plan: dict,
    payment_id: int,
    preview_end: datetime,
    back_cb: str,
    invoice_url: str
) -> None:
    """Создает и отправляет сообщение с инвойсом"""
    
    # Определяем режим
    is_extend = "extend" in back_cb or "ext_" in callback.data
    mode_label = "Продление туннеля" if is_extend else "Новый туннель"
    
    b = InlineKeyboardBuilder()
    b.button(text=f"💳 Оплатить {plan['price']} {CRYPTO_ASSET}", url=invoice_url)
    b.button(text="🔄 Проверить оплату", callback_data=f"check_payment_{payment_id}")
    b.button(text="◀️ Назад", callback_data=back_cb)
    b.adjust(1)
    
    text = (
        f"💳 <b>Счёт на оплату</b>\n\n"
        f"🔧 <b>Режим:</b> {mode_label}\n"
        f"📦 <b>Тариф:</b> {plan['name']}\n"
        f"💰 <b>Сумма:</b> {plan['price']} {CRYPTO_ASSET}\n"
        f"📅 <b>Активен до:</b> {preview_end.strftime('%d.%m.%Y')}\n"
        f"⏳ <b>Счёт действует:</b> 1 час\n\n"
        "Нажмите кнопку ниже — откроется @CryptoBot для оплаты.\n"
        "После оплаты нажмите <b>«Проверить оплату»</b>."
    )
    
    try:
        await callback.message.edit_text(text, reply_markup=b.as_markup())
    except Exception as e:
        await callback.message.answer(text, reply_markup=b.as_markup())


# ── Хендлеры ──────────────────────────────────────────────────────────────────

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
        # Создаем платеж и рассчитываем дату окончания
        payment_id, preview_end = await payment_service.create_payment(
            callback.from_user.id,
            plan_id
        )
        
        if not payment_id:
            await callback.message.answer("❌ Не удалось создать платеж")
            return
        
        # Создаем инвойс в CryptoBot
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
        
        # Обновляем invoice_id в БД
        with db.get_db() as conn:
            conn.execute(
                "UPDATE payments SET crypto_invoice_id=? WHERE id=?",
                (invoice.invoice_id, payment_id)
            )
        
        # Создаем сообщение с инвойсом
        await create_invoice_message(
            callback,
            plan_id,
            plan,
            payment_id,
            preview_end,
            "menu_vpn",
            invoice.pay_url
        )
        
        logger.info(f"Создан инвойс: plan={plan_id} payment={payment_id} invoice={invoice.invoice_id}")
        
    except Exception as e:
        logger.exception("Ошибка при создании инвойса")
        await callback.message.answer("❌ Произошла ошибка. Попробуйте позже.")


@router.callback_query(F.data.startswith("ext_vpn_"))
async def cb_ext_vpn(callback: CallbackQuery, bot: Bot, xui_client: AuthenticatedClient):
    """Обработчик продления существующего туннеля"""
    if not CRYPTO_BOT_TOKEN:
        await callback.answer("⚠️ Оплата временно недоступна", show_alert=True)
        return
    
    # Парсим callback_data: ext_vpn_{plan_id}_{user_id}
    parts = callback.data.removeprefix("ext_vpn_").rsplit("_", 1)
    if len(parts) != 2:
        await callback.answer("❌ Неверный формат", show_alert=True)
        return
    
    plan_id, user_id_str = parts
    if plan_id not in VPN_PLANS:
        await callback.answer("❌ Тариф не найден", show_alert=True)
        return
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        await callback.answer("❌ Неверный ID пользователя", show_alert=True)
        return
    
    await callback.answer("⏳ Создаём счёт...")
    
    payment_service = PaymentService(bot, xui_client)
    
    try:
        # Создаем платеж
        payment_id, preview_end = await payment_service.create_payment(
            callback.from_user.id,
            plan_id
        )
        
        if not payment_id:
            await callback.message.answer("❌ Не удалось создать платеж")
            return
        
        # Создаем инвойс
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
        
        # Обновляем invoice_id
        with db.get_db() as conn:
            conn.execute(
                "UPDATE payments SET crypto_invoice_id=? WHERE id=?",
                (invoice.invoice_id, payment_id)
            )
        
        # Создаем сообщение с инвойсом
        await create_invoice_message(
            callback,
            plan_id,
            plan,
            payment_id,
            preview_end,
            "menu_extend_vpn",
            invoice.pay_url
        )
        
        logger.info(f"Создан инвойс на продление: plan={plan_id} payment={payment_id}")
        
    except Exception as e:
        logger.exception("Ошибка при создании инвойса на продление")
        await callback.message.answer("❌ Произошла ошибка. Попробуйте позже.")


@router.callback_query(F.data.startswith("check_payment_"))
async def cb_check_payment(callback: CallbackQuery, bot: Bot, xui_client: AuthenticatedClient):
    """Обработчик проверки оплаты"""
    try:
        payment_id = int(callback.data.removeprefix("check_payment_"))
    except ValueError:
        await callback.answer("❌ Неверный ID платежа", show_alert=True)
        return
    
    await callback.answer("🔄 Проверяем статус...")
    
    # Получаем платеж из БД
    payment = db.get_payment(payment_id)
    
    if not payment:
        await callback.answer("❌ Платеж не найден", show_alert=True)
        return
    
    # Проверяем, что платеж принадлежит пользователю
    if payment["user_id"] != callback.from_user.id:
        await callback.answer("❌ Это не ваш платеж", show_alert=True)
        return
    
    # Проверяем статус в БД
    if payment["status"] == "paid":
        await callback.answer("✅ Уже оплачено — туннель активирован.", show_alert=True)
        return
    
    if payment["status"] in ("failed", "expired"):
        await callback.answer("❌ Счёт истёк. Создайте новый.", show_alert=True)
        return
    
    # Проверяем статус в CryptoBot
    invoices = await get_invoices([payment["crypto_invoice_id"]])
    if not invoices:
        await callback.answer("⚠️ Не удалось проверить статус. Попробуйте позже.", show_alert=True)
        return
    
    inv = invoices[0]
    
    if inv.status == "paid":
        await callback.answer("✅ Оплата найдена! Настраиваем VPN...")
        
        # Обрабатываем оплату
        payment_service = PaymentService(bot, xui_client)
        
        # Парсим payload для получения plan_id
        try:
            plan_id, _ = parse_payload(inv.payload)
        except ValueError:
            plan_id = list(VPN_PLANS.keys())[0] if VPN_PLANS else "basic"
        
        success = await payment_service.process_payment(
            payment_id=payment_id,
            invoice_id=inv.invoice_id,
            user_id=payment["user_id"],
            plan_id=plan_id,
            duration_days=payment["duration_days"],
            expires_at=datetime.now() + timedelta(days=payment["duration_days"])
        )
        
        if not success:
            await callback.message.answer(
                "❌ Не удалось активировать туннель. Обратитесь в @support"
            )
            
    elif inv.status == "expired":
        db.mark_payment_expired(payment_id)
        await callback.answer("❌ Счёт истёк. Создайте новый заказ.", show_alert=True)
    else:
        await callback.answer("⏳ Оплата ещё не поступила. Попробуйте через минуту.", show_alert=True)


@router.callback_query(F.data == "menu_extend_vpn")
async def cb_extend_vpn(callback: CallbackQuery, xui_client: AuthenticatedClient):
    """Показывает существующие туннели для продления"""
    try:
        result = await get_client(
            email=str(callback.from_user.id),
            client=xui_client
        )
        
        if not result or not result.success or not result.obj:
            await callback.answer("У тебя нет активного туннеля.", show_alert=True)
            return
        
        client_data = result.obj["client"]
        tunnel = TunnelInfo.from_api_response(client_data)
        
        if not tunnel.is_active:
            await callback.answer("У тебя нет активного туннеля.", show_alert=True)
            return
        
        expiry_text = tunnel.expiry_time.strftime("%d.%m.%Y") if tunnel.expiry_time else "Без ограничений"
        
        await callback.message.edit_text(
            "♻️ <b>Продление туннеля</b>\n\n"
            f"👥 Группа: <b>{tunnel.group}</b>\n"
            f"📅 Действует до: <b>{expiry_text}</b>\n\n"
            "Выбери срок продления:",
            reply_markup=kb_vpn_plans_extend(callback.from_user.id)
        )
        await callback.answer()
        
    except Exception as e:
        logger.exception("Ошибка получения туннеля из XUI")
        await callback.answer("Ошибка получения данных туннеля.", show_alert=True)


@router.callback_query(F.data.startswith("extend_tunnel_"))
async def cb_extend_tunnel(callback: CallbackQuery):
    """Обработчик выбора туннеля для продления"""
    try:
        user_id = int(callback.data.removeprefix("extend_tunnel_"))
    except ValueError:
        await callback.answer("❌ Неверный ID пользователя", show_alert=True)
        return
    
    # Получаем активные подписки пользователя
    subscriptions = db.get_active_subscriptions(user_id)
    
    if not subscriptions:
        await callback.answer("❌ Активных туннелей не найдено.", show_alert=True)
        return
    
    # Берем последнюю активную подписку
    latest_sub = subscriptions[0]
    sub_end = datetime.fromisoformat(latest_sub["expires_at"])
    
    await callback.message.edit_text(
        f"♻️ <b>Продление туннеля</b>\n\n"
        f"Текущая дата окончания: <b>{sub_end.strftime('%d.%m.%Y')}</b>\n\n"
        "Выбери тариф — дни прибавятся к этой дате:",
        reply_markup=kb_vpn_plans_extend(user_id)
    )
    await callback.answer()