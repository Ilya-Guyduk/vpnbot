import logging

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, InputFile

from aiogram.utils.keyboard import InlineKeyboardBuilder
from routers.utils import safe_edit
from keyboards.inline import kb_main
from services.xui_client.xui_client.client import AuthenticatedClient
from services.xui_client.xui_client.api.clients.get_panel_api_clients_list import (
    asyncio as get_clients_list,
)
from services.xui_client.xui_client.api.clients.get_panel_api_clients_get_email import (
    asyncio as get_client,
)
from routers.personal_accont.payment_service import TunnelInfo  # импортируем TunnelInfo

logger = logging.getLogger(__name__)
router = Router()
#router.include_router(extend_subs)


@router.callback_query(F.data.startswith("sub_details_"))
async def cb_tunnel_details(callback: CallbackQuery, xui_client: AuthenticatedClient) -> None:
    """
    Обработчик клика по кнопке туннеля в личном кабинете.
    Показывает детальную информацию о туннеле.
    """
    try:
        # Извлекаем ID туннеля
        tunnel_id = callback.data.removeprefix("sub_details_")
        
        # Получаем информацию о клиенте
        response = await get_clients_list(client=xui_client)
        
        if not response or not response.obj:
            await callback.answer("❌ Туннель не найден", show_alert=True)
            return
        
        # Ищем нужный туннель
        target_client = None
        for client in response.obj:
            if str(client.get("id")) == tunnel_id:
                target_client = client
                break
        
        if not target_client:
            await callback.answer("❌ Туннель не найден", show_alert=True)
            return
        
        # Форматируем детальную информацию
        client_data = TunnelInfo.from_api_response(target_client)
        
        # Создаем текст с деталями
        details_text = (
            f"📡 <b>Детали туннеля</b>\n\n"
            f"📧 <b>Name:</b> <code>{client_data.email}</code>\n"
            f"👥 <b>Группа:</b> {client_data.group}\n"
            f"🔐 <b>Статус:</b> {'🟢 Активен' if client_data.is_active else '🔴 Отключён'}\n"
            f"📅 <b>Действует до:</b> {client_data.expiry_time.strftime('%d.%m.%Y') if client_data.expiry_time else '♾️ Без ограничений'}\n"
            f"💾 <b>Трафик:</b> {client_data.total_gb} GB\n"
            f"🖥️ <b>Устройств:</b> {client_data.limit_ip if client_data.limit_ip > 0 else 'Без ограничений'}\n"
        )
        
        # Добавляем кнопки действий для туннеля
        b = InlineKeyboardBuilder()
        b.button(text="🔄 Продлить", callback_data=f"pay_type_subs_{client_data.email}")
        b.button(text="🔄 Конфиги", callback_data=f"subs_configs_{client_data.email}")
        b.button(text="📊 Статистика", callback_data=f"tunnel_stats_{client_data.client_id}")
        b.button(text="🔗 Получить ссылку", callback_data=f"get_sub_link_{client_data.client_id}")
        b.button(text="◀️ Назад", callback_data="menu_personal_account")
        b.adjust(2)
        
        await safe_edit(
            callback,
            details_text,
            reply_markup=b.as_markup()
        )
        
    except Exception as e:
        logger.exception("Failed to get tunnel details")
        await callback.answer("❌ Ошибка при получении деталей туннеля", show_alert=True)


@router.callback_query(F.data.startswith("get_sub_link_"))
async def cb_get_subscription_link(callback: CallbackQuery, xui_client: AuthenticatedClient):
    """Отправляет пользователю ссылку на подписку и QR-код"""
    try:
        tunnel_id = callback.data.removeprefix("get_sub_link_")
        
        # Получаем информацию о туннеле
        result = await get_client(
            email=str(callback.from_user.id),
            client=xui_client
        )
        
        if not result or not result.success or not result.obj:
            await callback.answer("❌ Туннель не найден", show_alert=True)
            return
        
        tunnel = TunnelInfo.from_api_response(result.obj)
        
        if not tunnel.sub_id:
            await callback.answer("❌ Ссылка на подписку не найдена", show_alert=True)
            return
        
        sub_link = tunnel.get_subscription_link()
        if not sub_link:
            await callback.answer("❌ Не удалось сформировать ссылку", show_alert=True)
            return
        
        qr_buffer = tunnel.get_qr_code()
        
        caption = (
            "🔗 <b>Ваша ссылка на подписку</b>\n\n"
            f"<code>{sub_link}</code>\n\n"
            "📱 Отсканируйте QR-код в приложении VPN:\n"
            "• V2RayNG\n"
            "• Shadowrocket\n"
            "• Hiddify\n"
            "• NekoBox"
        )
        
        if qr_buffer:
            await callback.message.delete()
            await callback.message.answer_photo(
                photo=InputFile(qr_buffer, filename="subscription_qr.png"),
                caption=caption,
                reply_markup=kb_main()
            )
        else:
            await callback.message.edit_text(
                caption,
                reply_markup=kb_main()
            )
            
    except Exception as e:
        logger.exception("Ошибка при получении ссылки на подписку")
        await callback.answer("❌ Ошибка при получении ссылки", show_alert=True)



