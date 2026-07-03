import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from routers.utils import safe_edit
from routers.personal_accont.payment_service import router as payment
from routers.personal_accont.sub_details.main import router as subs_details 


from services.xui_client.xui_client.client import AuthenticatedClient
from services.xui_client.xui_client.api.clients.get_panel_api_clients_list import (
    asyncio as get_clients_list,
)
logger = logging.getLogger(__name__)
router = Router()

#router.include_router(new_vpn_sub)
router.include_router(subs_details)
router.include_router(payment)



_PERSONAL_ACCOUNT_TEXT = (
    "👤 <b>Личный кабинет</b>\n\n"
    "Здесь вы можете управлять своими подключениями."
)


@router.callback_query(F.data == "menu_personal_account")
async def cb_personal_account(callback: CallbackQuery, xui_client: AuthenticatedClient) -> None:
    """Обработчик кнопки личного кабинета."""
    try:
        logger.debug(f"Запрос клиентов через XUI api:{xui_client._base_url}")
        # Получаем список всех клиентов
        response = await get_clients_list(
            client=xui_client,
        )
        logger.info(f"get_clients_list response from XUI: Succes:{response.success}, msg:{response.msg}, {len(response.obj)}")
        
        # Проверяем, есть ли клиенты
        if not response or not response.obj:
            await safe_edit(
                callback,
                _PERSONAL_ACCOUNT_TEXT + "\n\n❌ У вас нет активных подписок.\n\nНажмите «Новая подписка», чтобы оформить доступ.",
                reply_markup=kb_personal_account(subs=[])  # <-- передаем пустой список
            )
            return
        
        # Фильтруем клиенты по tgId
        user_id = str(callback.from_user.id)
        user_tunnels = []
        subs_for_keyboard = []  # <-- список для клавиатуры
        
        for client in response.obj:
            # tgId находится прямо в объекте клиента
            client_tg_id = client.get("tgId")
            
            if client_tg_id and str(client_tg_id) == user_id:
                user_tunnels.append(client)
                
                # Форматируем данные для клавиатуры
                expiry_time = client.get("expiryTime", 0)
                expiry_dt = None
                if expiry_time and expiry_time > 0:
                    expiry_dt = datetime.fromtimestamp(expiry_time / 1000)
                
                subs_for_keyboard.append({
                    "id": client.get("id"),
                    "email": client.get("email"),
                    "expiry": expiry_dt
                })
                
                logger.info(f"Found tunnel for user {user_id}: {client.get('email')}")
        
        if not user_tunnels:
            await safe_edit(
                callback,
                _PERSONAL_ACCOUNT_TEXT + "\n\n❌ У вас нет активных подписок.\n\nНажмите «Новая подписка», чтобы оформить доступ.",
                reply_markup=kb_personal_account(subs=[])  # <-- передаем пустой список
            )
            return
        
        # Если есть туннели, показываем их с клавиатурой
        tunnel_info = format_clients_info(user_tunnels)
        await safe_edit(
            callback,
            _PERSONAL_ACCOUNT_TEXT + "\n\n" + tunnel_info,
            reply_markup=kb_personal_account(subs=subs_for_keyboard)  # <-- передаем список
        )
        
    except Exception as e:
        logger.exception("XUI request failed")
        await safe_edit(
            callback,
            _PERSONAL_ACCOUNT_TEXT + "\n\n❌ Ошибка при получении данных о подписках. Попробуйте позже.",
            reply_markup=kb_personal_account(subs=[])  # <-- передаем пустой список
        )


def kb_personal_account(subs: list) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру личного кабинета
    
    Аргументы:
        subs: список подписок, каждая подписка - словарь с полями:
            - email: email туннеля
            - id: ID туннеля (опционально)
            - expiry: дата окончания (опционально)
    """
    b = InlineKeyboardBuilder()
    
    # Кнопка новой подписки
    b.button(text="🆕 Новая подписка", callback_data="pay_type_subs_")
    
    # Кнопки для каждой подписки
    for sub in subs:
        # Форматируем название кнопки
        email = sub.get('email', 'Туннель')
        expiry = sub.get('expiry')
        
        if expiry:
            # Если есть дата окончания, показываем её
            try:
                if isinstance(expiry, str):
                    expiry_dt = datetime.fromisoformat(expiry)
                else:
                    expiry_dt = expiry
                    
                days_left = (expiry_dt - datetime.now()).days
                if days_left > 0:
                    button_text = f"📡 {email} ({days_left} дн.)"
                else:
                    button_text = f"📡 {email} (🔴 истек)"
            except:
                button_text = f"📡 {email}"
        else:
            button_text = f"📡 {email}"
        
        # Создаем callback_data с ID туннеля или email
        tunnel_id = sub.get('id', email)
        b.button(
            text=button_text,
            callback_data=f"sub_details_{tunnel_id}"
        )
    
    # Кнопка помощи
    b.button(text="🆘 Помочь с установкой", callback_data="menu_help")
    
    # Кнопка назад
    b.button(text="◀️ Назад", callback_data="menu_main")
    
    # Расположение: 2 кнопки в ряду
    b.adjust(1)
    
    return b.as_markup()

##################################################################################################


def format_clients_info(clients: list) -> str:
    """Форматирует информацию о клиентах для отображения."""
    if not clients:
        return "❌ У вас нет активных подписок."
    
    lines = ["📡 <b>Ваши туннели</b>\n"]
    
    for i, client in enumerate(clients, 1):
        # Данные берутся напрямую из объекта клиента
        email = client.get("email", "Неизвестно")
        group = client.get("group") or "не указана"
        enabled = client.get("enable", False)
        expiry = client.get("expiryTime", 0)
        
        # Получаем трафик из вложенного объекта traffic
        traffic = client.get("traffic", {})
        up = traffic.get("up", 0)
        down = traffic.get("down", 0)
        traffic_gb = round((up + down) / 1024**3, 2)
        
        # Форматируем дату и статус
        if expiry and expiry > 0:
            expire_dt = datetime.fromtimestamp(expiry / 1000)
            days_left = (expire_dt - datetime.now()).days
            
            if days_left > 7:
                icon = "🟢"
            elif days_left > 0:
                icon = "🟡"
            else:
                icon = "🔴"
            
            expiry_text = f"{icon} <b>{expire_dt:%d.%m.%Y}</b> ({days_left} дн.)"
        else:
            expiry_text = "♾️ Без ограничений"
        
        # Статус
        status = "🟢 Активен" if enabled else "🔴 Отключён"
        
        # Собираем информацию о туннеле
        lines.append(
            f"<b>Туннель #{i}</b>\n"
            f"📧 Name: <code>{email}</code>\n"
            f"👥 Группа: <b>{group}</b>\n"
            f"📊 Использовано: <b>{traffic_gb:.2f} GB</b>\n"
            f"📅 Действует до: {expiry_text}\n"
            f"🔐 Статус: {status}\n"
        )
        
        if i < len(clients):
            lines.append("─" * 30 + "\n")
    
    return "\n".join(lines)

