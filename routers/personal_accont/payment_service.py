import logging
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any, List
import funkybob
import qrcode
from io import BytesIO
import hashlib
import base64

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message, InputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import VPN_PLANS, ADMIN_IDS, CRYPTO_ASSET, CRYPTO_BOT_TOKEN, XUI_API_HOST, XUI_SUB_PORT, XUI_SUB_PATH
from database import db
from keyboards.inline import kb_main
from services.cryptobot import get_invoices
from services.xui_client.xui_client.models.client import Client
from services.xui_client.xui_client.models.post_panel_api_clients_add_body import PostPanelApiClientsAddBody

from services.xui_client.xui_client.client import AuthenticatedClient
from services.xui_client.xui_client.api.clients.get_panel_api_clients_get_email import (
    asyncio as get_client,
)
from services.xui_client.xui_client.api.clients.post_panel_api_clients_add import (
    asyncio as create_client,
)
from services.xui_client.xui_client.api.clients.post_panel_api_clients_update_email import (
    asyncio as update_client,
)

logger = logging.getLogger(__name__)
router = Router()

# Константы
SEP = "|"
INVOICE_EXPIRY_SECONDS = 3600


def generate_sub_id(email: str, tg_id: str) -> str:
    """
    Генерирует уникальный subId для пользователя
    
    Формат: {tg_id}_{hash}
    """
    # Берем email или tg_id как основу
    base = f"{tg_id}_{email}_{datetime.now().timestamp()}"
    
    # Создаем хеш
    hash_obj = hashlib.sha256(base.encode())
    hash_hex = hash_obj.hexdigest()[:16]
    
    return f"{tg_id}_{hash_hex}"


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
    tg_id: int
    total_gb: int

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'TunnelInfo':
        """Создает объект из ответа API 3x-ui"""
        expiry_ms = data.get("expiryTime", 0)
        expiry_time = datetime.fromtimestamp(expiry_ms / 1000) if expiry_ms > 0 else None
        
        return cls(
            client_id=str(data.get("id", "")),
            email=data.get("email", ""),
            group=data.get("group", "-"),
            expiry_time=expiry_time,
            is_active=data.get("enable", False),
            comment=data.get("comment", ""),
            limit_ip=data.get("limitIp", 0),
            reset=data.get("reset", 0),
            security=data.get("security", "auto"),
            sub_id=data.get("subId", ""),
            tg_id=str(data.get("tgId", "")),
            total_gb=data.get("totalGB", 0),
        )
    
    def get_subscription_link(self) -> Optional[str]:
        """Формирует ссылку на подписку"""
        if not self.sub_id:
            return None
        return f"{XUI_API_HOST}:{XUI_SUB_PORT}{XUI_SUB_PATH}{self.sub_id}"
    
    def get_qr_code(self) -> Optional[BytesIO]:
        """Генерирует QR-код для ссылки подписки"""
        link = self.get_subscription_link()
        if not link:
            return None
        
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=8,
                border=4,
            )
            qr.add_data(link)
            qr.make(fit=True)
            
            img = qr.make_image(fill_color="black", back_color="white")
            
            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            
            return buffer
        except Exception as e:
            logger.error(f"Ошибка при генерации QR-кода: {e}")
            return None


class PaymentService:
    """Сервис для работы с платежами"""
    
    def __init__(self, bot: Bot, xui_client: AuthenticatedClient):
        self.bot = bot
        self.xui_client = xui_client
    
    async def create_payment(
        self, 
        tg_id: int, 
        plan_id: str,
        parent_tunnel_id: Optional[int] = None,
        is_extend: bool = False
    ) -> Tuple[Optional[int], Optional[datetime]]:
        """Создает платеж в БД"""
        logger.debug(f"create_payment tg_id:{tg_id}, plan_id:{plan_id}, parent_tunnel_id:{parent_tunnel_id}, is_extend:{is_extend}")

        plan = VPN_PLANS[plan_id]
        new_sub_end = await self._calculate_new_sub_end(tg_id, plan["duration"], is_extend)
        
        logger.info(f"create_payment Создаём платеж в БД: tg_id:{tg_id} plan:{plan}, is_extend:{is_extend}")
        payment_id = db.create_payment(
            user_id=tg_id,
            duration_days=plan["duration"],
            amount_rub=plan.get("price_rub", 0),
            amount_crypto=str(plan["price"]),
            crypto_asset=CRYPTO_ASSET,
            crypto_invoice_id=0
        )
        
        return payment_id, new_sub_end
    
    async def process_payment(
        self, 
        payment_id: int, 
        user_id: int,
        plan_id: str,
        duration_days: int,
        expires_at: datetime,
        is_extend: bool = False,  # <-- используем этот параметр
        parent_tunnel_id: Optional[int] = None,
        invoice_id: Optional[int] = None
        
    ) -> bool:
        """Обрабатывает успешную оплату"""
        try:
            plan = VPN_PLANS[plan_id]
            user_id_str = str(user_id)
            
            # Генерируем subId
            sub_id = generate_sub_id(user_id_str, user_id_str)
            logger.info(f"Сгенерирован subId для {user_id}: {sub_id}")
            
            # Получаем существующий туннель ТОЛЬКО если это продление
            tunnel_info = None
            if is_extend:
                tunnel_info = await self._get_tunnel_info(user_id_str)
            
            # Используем переданный флаг is_extend
            if is_extend and tunnel_info and tunnel_info.is_active:
                # Обновляем существующий туннель
                if tunnel_info.expiry_time and tunnel_info.expiry_time > datetime.now():
                    new_expiry = tunnel_info.expiry_time + timedelta(days=duration_days)
                else:
                    new_expiry = datetime.now() + timedelta(days=duration_days)
                    
                await self._update_tunnel(tunnel_info.email, new_expiry, sub_id)
                logger.info(f"Продлен туннель для {user_id} до {new_expiry}")
            else:
                # Создаем новый туннель
                new_expiry = datetime.now() + timedelta(days=duration_days)
                await self._create_new_tunnel(user_id_str, new_expiry, sub_id)
                logger.info(f"Создан новый туннель для {user_id} до {new_expiry}")
            
            # Отмечаем платеж как оплаченный
            db.mark_payment_paid(payment_id, new_expiry)
            
            # Получаем обновленную информацию о туннеле
            updated_tunnel = await self._get_tunnel_by_sub_id(sub_id)
            
            # Если не нашли по sub_id, пробуем найти по user_id
            if not updated_tunnel:
                updated_tunnel = await self._get_tunnel_info(user_id_str)
            
            # Уведомляем пользователя с QR-кодом и ссылкой
            if updated_tunnel:
                await self._notify_user_with_subscription(user_id, new_expiry, updated_tunnel)
            else:
                await self._notify_user_fallback(user_id, new_expiry)
            
            # Уведомляем админов
            await self._notify_admins(user_id, plan, payment_id, invoice_id, new_expiry)
            
            return True
            
        except Exception as e:
            logger.exception(f"Ошибка при обработке оплаты payment_id={payment_id}")
            db.mark_payment_failed(payment_id)
            return False
        
    async def _calculate_new_sub_end(self, user_id: int, add_days: int, is_extend: bool = False) -> datetime:
        """Рассчитывает новую дату окончания подписки"""
        now = datetime.now()
        
        # Если это НОВАЯ подписка - всегда начинаем с today
        if not is_extend:
            new_end = now + timedelta(days=add_days)
            logger.info("Новый туннель до %s (%d дн.)",
                    new_end.strftime("%d.%m.%Y"), 
                    add_days)
            return new_end
        
        # Если это ПРОДЛЕНИЕ - учитываем существующий туннель
        try:
            tunnel_info = await self._get_tunnel_info(str(user_id))
            if tunnel_info and tunnel_info.is_active and tunnel_info.expiry_time and tunnel_info.expiry_time > now:
                new_end = tunnel_info.expiry_time + timedelta(days=add_days)
                logger.info("Продление существующего туннеля: %s → %s (+%d дн.)",
                        tunnel_info.expiry_time.strftime("%d.%m.%Y"),
                        new_end.strftime("%d.%m.%Y"),
                        add_days)
                return new_end
        except Exception as e:
            logger.warning(f"Не удалось получить информацию о туннеле: {e}")
        
        # Fallback: если не нашли туннель, начинаем с today
        new_end = now + timedelta(days=add_days)
        logger.info("Новый туннель до %s (%d дн.)",
                new_end.strftime("%d.%m.%Y"), 
                add_days)
        return new_end
    
    async def _get_tunnel_by_sub_id(self, sub_id: str) -> Optional[TunnelInfo]:
        """Получает информацию о туннеле по sub_id"""
        try:
            from services.xui_client.xui_client.api.clients.get_panel_api_clients_list import (
                asyncio as get_clients_list,
            )
            
            list_response = await get_clients_list(client=self.xui_client)
            
            if list_response and list_response.obj:
                for client in list_response.obj:
                    if client.get("subId", "") == sub_id:
                        return TunnelInfo.from_api_response(client)
            
            return None
            
        except Exception as e:
            logger.warning(f"Не удалось получить туннель по sub_id {sub_id}: {e}")
            return None

    async def _get_tunnel_info(self, tg_id: str) -> Optional[TunnelInfo]:
        """
        Получает информацию о туннеле из 3x-ui по user_id
        
        Ищет только по tgId (активные туннели)
        """
        try:
            # Пытаемся найти по email (если email = user_id)
            result = await get_client(
                email=tg_id,
                client=self.xui_client
            )
            
            if result and result.success and result.obj:
                tunnel = TunnelInfo.from_api_response(result.obj)
                if tunnel.is_active:
                    return tunnel
            
            # Если не нашли по email, ищем среди всех клиентов по tgId
            from services.xui_client.xui_client.api.clients.get_panel_api_clients_list import (
                asyncio as get_clients_list,
            )
            
            list_response = await get_clients_list(client=self.xui_client)
            
            if list_response and list_response.obj:
                for client in list_response.obj:
                    # Проверяем tgId
                    client_tg_id = client.get("tgId", 0)
                    if str(client_tg_id) == tg_id:
                        tunnel = TunnelInfo.from_api_response(client)
                        if tunnel.is_active:
                            return tunnel
            
            return None
            
        except Exception as e:
            logger.warning(f"Не удалось получить туннель для user_id {tg_id}: {e}")
            return None
    
    async def _update_tunnel(self, email: str, new_expiry: datetime, sub_id: str):
        """Обновляет существующий туннель"""
        try:
            current_tunnel = await self._get_tunnel_info(email)
            
            if current_tunnel:
                client_obj = Client(
                    id=current_tunnel.client_id,
                    email=email,
                    expiry_time=int(new_expiry.timestamp() * 1000),
                    enable=True,
                    group=current_tunnel.group,
                    comment=current_tunnel.comment,
                    limit_ip=current_tunnel.limit_ip,
                    reset=current_tunnel.reset,
                    security=current_tunnel.security,
                    sub_id=sub_id,  # Обновляем sub_id
                    tg_id=int(current_tunnel.tg_id),
                    total_gb=current_tunnel.total_gb
                )
                
                logger.info(f"Обновляем туннель {email} до {new_expiry.strftime('%d.%m.%Y')} с sub_id={sub_id}")
                
                result = await update_client(
                    email=email,
                    client=self.xui_client,
                    body=client_obj
                )
                
                if result and result.success:
                    logger.info(f"Обновлен туннель {email}")
                else:
                    error_msg = result.msg if result else "No response"
                    logger.error(f"Ошибка при обновлении туннеля {email}: {error_msg}")
                    raise Exception(f"Failed to update tunnel: {error_msg}")
            else:
                logger.warning(f"Туннель {email} не найден для обновления")
                
        except Exception as e:
            logger.error(f"Ошибка при обновлении туннеля {email}: {e}")
            raise

    async def _create_new_tunnel(self, email: str, new_expiry: datetime, sub_id: str):
        """Создает новый туннель"""
        try:
            generator = funkybob.RandomNameGenerator()
            it = iter(generator)
            random_name = next(it)
            
            client_data = {
                "email": random_name,  # Случайное имя для 3x-ui
                "expiryTime": int(new_expiry.timestamp() * 1000),
                "enable": True,
                "limitIp": 0,
                "totalGB": 0,
                "tgId": int(email) if email.isdigit() else 0,  # Сохраняем user_id в tgId
                "group": "vpn_users",
                "security": "auto",
                "comment": f"Создан автоматически для {email}",  # Сохраняем user_id в комментарии
                "reset": 0,
                "subId": sub_id
            }
            
            inbound_ids = [4, 6, 9, 11, 13, 19, 21, 22, 26, 28, 33, 46, 48, 49, 50, 51, 52, 56, 1, 14, 15, 18, 20, 23, 25, 27, 29, 38, 39, 40, 41, 42, 43, 45, 53, 55]
            
            logger.info(f"Создаем туннель для {email} с sub_id={sub_id}, random_name={random_name}")
            
            body = PostPanelApiClientsAddBody()
            body["client"] = client_data
            body["inboundIds"] = inbound_ids
            
            result = await create_client(
                client=self.xui_client,
                body=body
            )
            
            if result and result.success:
                logger.info(f"Создан новый туннель для {email} до {new_expiry.strftime('%d.%m.%Y')}")
                # Сохраняем в БД связь между user_id и email туннеля
                db.save_tunnel_mapping(
                    user_id=int(email) if email.isdigit() else 0,
                    tunnel_email=random_name,
                    sub_id=sub_id
                )
            else:
                error_msg = result.msg if result else "Unknown error"
                logger.error(f"Ошибка при создании туннеля: {error_msg}")
                raise Exception(f"API error: {error_msg}")
            
        except Exception as e:
            logger.error(f"Ошибка при создании туннеля {email}: {e}")
            raise
    
    async def _notify_user_with_subscription(self, user_id: int, expiry_date: datetime, tunnel: Optional[TunnelInfo]):
        """Уведомляет пользователя с QR-кодом и ссылкой на подписку"""
        try:
            if not tunnel or not tunnel.sub_id:
                # Если нет sub_id, отправляем простое уведомление
                await self._notify_user_fallback(user_id, expiry_date)
                return
            
            # Получаем ссылку на подписку
            sub_link = tunnel.get_subscription_link()
            if not sub_link:
                await self._notify_user_fallback(user_id, expiry_date)
                return
            
            # Генерируем QR-код
            qr_buffer = tunnel.get_qr_code()
            
            # Формируем сообщение
            caption = (
                "✅ <b>Туннель активирован!</b>\n\n"
                f"📅 <b>Активен до:</b> {expiry_date.strftime('%d.%m.%Y')}\n\n"
                "📱 <b>Ссылка для подключения:</b>\n"
                f"<code>{sub_link}</code>\n\n"
                "📖 <b>Инструкция по подключению:</b>\n"
                "1️⃣ Скачайте приложение для VPN (V2RayNG, Shadowrocket, Hiddify, NekoBox)\n"
                "2️⃣ Отсканируйте QR-код или вставьте ссылку вручную\n"
                "3️⃣ Нажмите «Подключиться»\n\n"
                "🔗 <b>Или используйте ссылку подписки:</b>\n"
                f"<code>{sub_link}</code>"
            )
            
            # Отправляем с QR-кодом
            if qr_buffer:
                await self.bot.send_photo(
                    user_id,
                    photo=InputFile(qr_buffer, filename="subscription_qr.png"),
                    caption=caption,
                    reply_markup=kb_main()
                )
            else:
                # Если QR не сгенерировался, отправляем только текст
                await self.bot.send_message(
                    user_id,
                    caption,
                    reply_markup=kb_main()
                )
                
        except Exception as e:
            logger.warning(f"Не удалось уведомить пользователя {user_id} с QR: {e}")
            await self._notify_user_fallback(user_id, expiry_date)
    
    async def _notify_user_fallback(self, user_id: int, expiry_date: datetime):
        """Fallback уведомление без QR-кода"""
        try:
            await self.bot.send_message(
                user_id,
                "✅ <b>Туннель активирован.</b>\n\n"
                f"📅 <b>Активен до:</b> {expiry_date.strftime('%d.%m.%Y')}\n\n"
                "📖 Как подключиться — раздел «Руководства».\n"
                "Ссылка для подписки доступна в личном кабинете.",
                reply_markup=kb_main()
            )
        except Exception as e:
            logger.warning(f"Не удалось уведомить пользователя {user_id}: {e}")
    
    async def _notify_user(self, user_id: int, expiry_date: datetime):
        """Старое уведомление (сохранено для совместимости)"""
        await self._notify_user_fallback(user_id, expiry_date)
    
    async def _notify_admins(
        self, 
        user_id: int, 
        plan: dict, 
        payment_id: int,
        invoice_id: Optional[int],
        new_sub_end: datetime
    ):
        """Уведомляет админов о продаже"""
        text = (
            f"💰 Новая продажа (CryptoBot)\n"
            f"User: {user_id} | Тариф: {plan['name']}\n"
            f"Сумма: {plan['price']} {CRYPTO_ASSET}\n"
            f"Активен до: {new_sub_end.strftime('%d.%m.%Y')}\n"
            f"Payment: {payment_id} | Invoice: {invoice_id or 'N/A'}"
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
    invoice_url: str,
    is_extend: bool = False  # <-- добавляем параметр
) -> None:
    """Создает и отправляет сообщение с инвойсом"""
    logger.debug(f"")
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

@router.callback_query(F.data.startswith("check_payment_"))
async def cb_check_payment(callback: CallbackQuery, bot: Bot, xui_client: AuthenticatedClient):
    """Обработчик проверки оплаты"""
    try:
        payment_id = int(callback.data.removeprefix("check_payment_"))
    except ValueError:
        await callback.answer("❌ Неверный ID платежа", show_alert=True)
        return
    
    await callback.answer("🔄 Проверяем статус...")
    
    payment = db.get_payment(payment_id)
    
    if not payment:
        await callback.answer("❌ Платеж не найден", show_alert=True)
        return
    
    if payment["user_id"] != callback.from_user.id:
        await callback.answer("❌ Это не ваш платеж", show_alert=True)
        return
    
    if payment["status"] == "paid":
        await callback.answer("✅ Уже оплачено — туннель активирован.", show_alert=True)
        return
    
    if payment["status"] in ("failed", "expired"):
        await callback.answer("❌ Счёт истёк. Создайте новый.", show_alert=True)
        return
    
    invoices = await get_invoices([payment["crypto_invoice_id"]])
    if not invoices:
        await callback.answer("⚠️ Не удалось проверить статус. Попробуйте позже.", show_alert=True)
        return
    
    inv = invoices[0]
    
    if inv.status == "paid":
        await callback.answer("✅ Оплата найдена! Настраиваем VPN...")
        
        payment_service = PaymentService(bot, xui_client)
        
        try:
            plan_id, _ = parse_payload(inv.payload)
        except ValueError:
            plan_id = list(VPN_PLANS.keys())[0] if VPN_PLANS else "basic"
        
        success = await payment_service.process_payment(
            payment_id=payment_id,
            user_id=payment["user_id"],
            plan_id=plan_id,
            duration_days=payment["duration_days"],
            expires_at=datetime.now() + timedelta(days=payment["duration_days"]),
            invoice_id=inv.invoice_id
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


