import asyncio
import logging
import os
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
import sqlite3
from contextlib import contextmanager

# Загрузка переменных окружения из .env
load_dotenv()

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Конфигурация из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
PAYMENT_PROVIDER_TOKEN = os.getenv("PAYMENT_PROVIDER_TOKEN", "")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()]

# Проверка обязательных переменных
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не задан в .env файле!")
if not ADMIN_IDS:
    logger.warning("ADMIN_IDS не задан — админ-команды будут недоступны")

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

# База данных
@contextmanager
def get_db():
    conn = sqlite3.connect('vpn_bot.db')
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Таблица пользователей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                subscription_end TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Таблица VPN-ключей
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vpn_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_value TEXT NOT NULL,
                duration_days INTEGER NOT NULL,
                is_used BOOLEAN DEFAULT 0,
                assigned_to INTEGER,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assigned_to) REFERENCES users (user_id)
            )
        ''')
        
        # Таблица заказов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                amount INTEGER,
                duration_days INTEGER,
                status TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')

# VPN тарифы
VPN_PLANS = {
    "basic_1m": {"name": "Базовый на 1 месяц", "price": 300, "duration": 30},
    "premium_1m": {"name": "Премиум на 1 месяц", "price": 500, "duration": 30},
    "premium_3m": {"name": "Премиум на 3 месяца", "price": 1200, "duration": 90},
    "premium_1y": {"name": "Премиум на 1 год", "price": 3500, "duration": 365},
}

# Инструменты для обхода цензуры
CENSORSHIP_TOOLS = {
    "vpn": "VPN-сервисы для безопасного подключения",
    "tor": "Tor Browser - анонимный браузер",
    "mirrors": "Актуальные зеркала заблокированных сайтов",
    "dns": "Настройка DNS для обхода блокировок",
    "proxy": "Прокси-серверы и расширения",
}

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔒 VPN-сервисы", callback_data="menu_vpn")
    builder.button(text="🛠 Другие инструменты", callback_data="menu_tools")
    builder.button(text="📖 Руководства", callback_data="menu_guides")
    builder.button(text="❓ Помощь", callback_data="menu_help")
    builder.adjust(2, 2)
    return builder.as_markup()

def get_vpn_plans_keyboard():
    builder = InlineKeyboardBuilder()
    for plan_id, plan in VPN_PLANS.items():
        builder.button(
            text=f"{plan['name']} - {plan['price']}₽", 
            callback_data=f"buy_vpn_{plan_id}"
        )
    builder.button(text="◀️ Назад", callback_data="menu_main")
    builder.adjust(1)
    return builder.as_markup()

def get_tools_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🌐 Tor Browser", callback_data="tool_tor")
    builder.button(text="🔄 Зеркала сайтов", callback_data="tool_mirrors")
    builder.button(text="🔧 DNS-настройки", callback_data="tool_dns")
    builder.button(text="🌍 Прокси", callback_data="tool_proxy")
    builder.button(text="◀️ Назад", callback_data="menu_main")
    builder.adjust(2, 2, 1)
    return builder.as_markup()

def get_guides_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="📱 Android", callback_data="guide_android")
    builder.button(text="🍎 iOS", callback_data="guide_ios")
    builder.button(text="💻 Windows", callback_data="guide_windows")
    builder.button(text="🐧 Linux", callback_data="guide_linux")
    builder.button(text="◀️ Назад", callback_data="menu_main")
    builder.adjust(2, 2, 1)
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Регистрируем пользователя
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR IGNORE INTO users (user_id, username, first_name)
            VALUES (?, ?, ?)
        ''', (message.from_user.id, message.from_user.username, message.from_user.first_name))
    
    welcome_text = (
        "🛡 <b>Бот для доступа к свободному интернету</b>\n\n"
        "Здесь вы найдёте инструменты для обхода цензуры и сохранения приватности:\n\n"
        "• Надёжные VPN-сервисы\n"
        "• Актуальные зеркала сайтов\n"
        "• Tor Browser и прокси\n"
        "• Подробные руководства\n\n"
        "Выберите интересующий раздел:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

@dp.message(Command("admin"))
async def cmd_admin(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔️ Доступ запрещён")
        return
    
    admin_text = (
        "👨‍💼 <b>Админ-панель</b>\n\n"
        "Команды:\n"
        "/add_keys - добавить VPN-ключи\n"
        "/stats - статистика\n"
        "/broadcast - рассылка"
    )
    await message.answer(admin_text)

@dp.message(Command("add_keys"))
async def cmd_add_keys(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    # Формат: /add_keys 30 KEY123,KEY456,KEY789
    try:
        parts = message.text.split(maxsplit=2)
        duration = int(parts[1])
        keys = parts[2].split(',')
        
        with get_db() as conn:
            cursor = conn.cursor()
            for key in keys:
                cursor.execute(
                    'INSERT INTO vpn_keys (key_value, duration_days) VALUES (?, ?)',
                    (key.strip(), duration)
                )
        
        await message.answer(f"✅ Добавлено {len(keys)} ключей на {duration} дней")
    except Exception as e:
        await message.answer(f"❌ Ошибка: {str(e)}\nФормат: /add_keys ДНИ KEY1,KEY2,KEY3")

@dp.message(Command("stats"))
async def cmd_stats(message: Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM users')
        total_users = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM vpn_keys WHERE is_used = 0')
        available_keys = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM orders WHERE status = "paid"')
        total_orders = cursor.fetchone()[0]
        
        stats_text = (
            f"📊 <b>Статистика</b>\n\n"
            f"👥 Пользователей: {total_users}\n"
            f"🔑 Свободных ключей: {available_keys}\n"
            f"💰 Оплаченных заказов: {total_orders}"
        )
        await message.answer(stats_text)

@dp.callback_query(F.data == "menu_main")
async def show_main_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "🛡 Выберите раздел:",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "menu_vpn")
async def show_vpn_menu(callback: CallbackQuery):
    text = (
        "🔒 <b>VPN-сервисы</b>\n\n"
        "Выберите подходящий тариф. После оплаты вы получите готовый ключ для подключения.\n\n"
        "<i>Все VPN-серверы находятся в юрисдикциях с уважением к приватности.</i>"
    )
    await callback.message.edit_text(text, reply_markup=get_vpn_plans_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "menu_tools")
async def show_tools_menu(callback: CallbackQuery):
    text = "🛠 <b>Другие инструменты обхода цензуры:</b>"
    await callback.message.edit_text(text, reply_markup=get_tools_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "menu_guides")
async def show_guides_menu(callback: CallbackQuery):
    text = "📖 <b>Руководства по настройке:</b>\nВыберите вашу платформу:"
    await callback.message.edit_text(text, reply_markup=get_guides_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "menu_help")
async def show_help(callback: CallbackQuery):
    help_text = (
        "❓ <b>Помощь</b>\n\n"
        "1. Выберите инструмент из меню\n"
        "2. Для VPN - оплатите тариф и получите ключ\n"
        "3. Следуйте инструкциям по настройке\n\n"
        "По техническим вопросам: @support"
    )
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад", callback_data="menu_main")
    await callback.message.edit_text(help_text, reply_markup=builder.as_markup())
    await callback.answer()

# Обработчики инструментов
@dp.callback_query(F.data.startswith("tool_"))
async def show_tool_info(callback: CallbackQuery):
    tool = callback.data.replace("tool_", "")
    tool_info = {
        "tor": (
            "🌐 <b>Tor Browser</b>\n\n"
            "Tor — это браузер для анонимного доступа в интернет. "
            "Он маршрутизирует ваш трафик через несколько слоёв шифрования.\n\n"
            "Скачать: torproject.org/download/\n"
            "На русском: torproject.org/ru/download/"
        ),
        "mirrors": (
            "🔄 <b>Зеркала заблокированных сайтов</b>\n\n"
            "Мы поддерживаем актуальный список зеркал популярных ресурсов.\n"
            "Отправьте боту название сайта чтобы получить зеркало."
        ),
        "dns": (
            "🔧 <b>Настройка DNS</b>\n\n"
            "Используйте защищённые DNS-серверы для обхода блокировок:\n"
            "• Cloudflare: 1.1.1.1\n"
            "• Quad9: 9.9.9.9\n"
            "• AdGuard DNS: 94.140.14.14"
        ),
        "proxy": (
            "🌍 <b>Прокси-серверы</b>\n\n"
            "Рекомендуемые расширения:\n"
            "• Proxy SwitchyOmega (Chrome/Firefox)\n"
            "• FoxyProxy (Firefox)\n\n"
            "Надёжные прокси-провайдеры в канале @proxy_list"
        )
    }
    
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад к инструментам", callback_data="menu_tools")
    
    await callback.message.edit_text(
        tool_info.get(tool, "Информация временно недоступна"),
        reply_markup=builder.as_markup(),
        link_preview_options=types.LinkPreviewOptions(is_disabled=True)
    )
    await callback.answer()

# Обработчики руководств
@dp.callback_query(F.data.startswith("guide_"))
async def show_guide(callback: CallbackQuery):
    platform = callback.data.replace("guide_", "")
    guides = {
        "android": (
            "📱 <b>Настройка VPN на Android</b>\n\n"
            "1. Скачайте приложение WireGuard из Google Play\n"
            "2. Нажмите '+' и выберите 'Создать из QR-кода'\n"
            "3. Отсканируйте QR-код, который мы пришлём после покупки VPN\n"
            "4. Нажмите на переключатель для подключения\n\n"
            "Альтернатива: используйте OpenVPN Connect"
        ),
        "ios": (
            "🍎 <b>Настройка VPN на iOS</b>\n\n"
            "1. Установите WireGuard из App Store\n"
            "2. Откройте конфигурационный файл из Telegram\n"
            "3. Нажмите 'Поделиться' → WireGuard\n"
            "4. Добавьте конфигурацию и подключитесь"
        ),
        "windows": (
            "💻 <b>Настройка VPN на Windows</b>\n\n"
            "1. Скачайте WireGuard с wireguard.com/install/\n"
            "2. Нажмите 'Add Tunnel' → 'Add empty tunnel...'\n"
            "3. Вставьте полученную конфигурацию\n"
            "4. Нажмите 'Activate'"
        ),
        "linux": (
            "🐧 <b>Настройка VPN на Linux</b>\n\n"
            "Ubuntu/Debian:\n"
            "<code>sudo apt install wireguard</code>\n\n"
            "Создайте файл /etc/wireguard/wg0.conf\n"
            "Запустите: <code>sudo wg-quick up wg0</code>"
        )
    }
    
    builder = InlineKeyboardBuilder()
    builder.button(text="◀️ Назад к руководствам", callback_data="menu_guides")
    
    await callback.message.edit_text(
        guides.get(platform, "Инструкция в разработке"),
        reply_markup=builder.as_markup()
    )
    await callback.answer()

# Логика покупки VPN
@dp.callback_query(F.data.startswith("buy_vpn_"))
async def process_vpn_purchase(callback: CallbackQuery):
    plan_id = callback.data.replace("buy_vpn_", "")
    
    if plan_id not in VPN_PLANS:
        await callback.answer("❌ Тариф не найден")
        return
    
    if not PAYMENT_PROVIDER_TOKEN:
        await callback.answer("⚠️ Оплата временно недоступна", show_alert=True)
        return
    
    plan = VPN_PLANS[plan_id]
    
    # Отправляем счёт на оплату
    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=plan["name"],
        description="VPN-подписка для обхода цензуры",
        payload=f"vpn_{plan_id}_{callback.from_user.id}",
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency="RUB",
        prices=[
            LabeledPrice(label=plan["name"], amount=plan["price"] * 100)  # В копейках
        ],
        start_parameter="vpn_subscription",
        need_name=False,
        need_phone_number=False,
        need_email=True,
        need_shipping_address=False
    )
    
    await callback.answer("💳 Счёт отправлен в чат")

@dp.pre_checkout_query()
async def process_pre_checkout(pre_checkout_query: PreCheckoutQuery):
    # Парсим plan_id из payload (формат: vpn_basic_1m_userid)
    payload_parts = pre_checkout_query.invoice_payload.split("_")
    
    try:
        plan_id = f"{payload_parts[1]}_{payload_parts[2]}" if len(payload_parts) > 3 else payload_parts[1]
    except IndexError:
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="❌ Ошибка обработки заказа. Попробуйте позже."
        )
        return
    
    if plan_id not in VPN_PLANS:
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="❌ Тариф не найден. Попробуйте позже."
        )
        return
    
    # Проверяем наличие ключей перед списанием
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(
            'SELECT COUNT(*) FROM vpn_keys WHERE is_used = 0 AND duration_days = ?',
            (VPN_PLANS[plan_id]["duration"],)
        )
        available = cursor.fetchone()[0]
    
    if available > 0:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    else:
        await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="❌ Извините, ключи для этого тарифа закончились. Попробуйте позже."
        )

@dp.message(F.successful_payment)
async def process_successful_payment(message: Message):
    payment = message.successful_payment
    payload = payment.invoice_payload
    email = payment.order_info.email if payment.order_info else "Не указан"
    
    # Извлекаем информацию из payload
    payload_parts = payload.split("_")
    
    try:
        plan_id = f"{payload_parts[1]}_{payload_parts[2]}" if len(payload_parts) > 3 else payload_parts[1]
    except IndexError:
        plan_id = None
    
    if plan_id not in VPN_PLANS:
        await message.answer(
            "❌ Произошла ошибка при обработке платежа. Свяжитесь с поддержкой: @support",
            reply_markup=get_main_keyboard()
        )
        for admin_id in ADMIN_IDS:
            try:
                await bot.send_message(
                    admin_id,
                    f"⚠️ КРИТИЧЕСКАЯ ОШИБКА!\n"
                    f"Оплата прошла, но не удалось определить тариф.\n"
                    f"Пользователь: {message.from_user.id}\n"
                    f"Payload: {payload}\n"
                    f"Сумма: {payment.total_amount // 100}₽"
                )
            except:
                pass
        return
    
    with get_db() as conn:
        cursor = conn.cursor()
        
        # Получаем свободный ключ
        cursor.execute(
            '''SELECT id, key_value FROM vpn_keys 
               WHERE is_used = 0 AND duration_days = ? 
               ORDER BY id LIMIT 1''',
            (VPN_PLANS[plan_id]["duration"],)
        )
        key_row = cursor.fetchone()
        
        if key_row:
            # Назначаем ключ пользователю
            subscription_end = datetime.now() + timedelta(days=VPN_PLANS[plan_id]["duration"])
            
            cursor.execute(
                'UPDATE vpn_keys SET is_used = 1, assigned_to = ? WHERE id = ?',
                (message.from_user.id, key_row['id'])
            )
            
            cursor.execute(
                '''UPDATE users SET subscription_end = ? WHERE user_id = ?''',
                (subscription_end.isoformat(), message.from_user.id)
            )
            
            # Сохраняем заказ
            cursor.execute(
                '''INSERT INTO orders (user_id, amount, duration_days, status) 
                   VALUES (?, ?, ?, 'paid')''',
                (message.from_user.id, payment.total_amount // 100, VPN_PLANS[plan_id]["duration"])
            )
            
            # Отправляем ключ
            config_text = f"""
🔑 <b>Ваш VPN-ключ готов!</b>

<b>Ключ конфигурации:</b>
<code>{key_row['key_value']}</code>

📅 <b>Действует до:</b> {subscription_end.strftime('%d.%m.%Y')}
📧 <b>Email:</b> {email}

<b>Инструкции по настройке:</b>
• Откройте раздел "Руководства" в меню бота
• Выберите вашу платформу
• Следуйте пошаговой инструкции

При возникновении проблем: @support
"""
            
            await message.answer(config_text, reply_markup=get_main_keyboard())
            
            # Уведомление админам
            for admin_id in ADMIN_IDS:
                try:
                    await bot.send_message(
                        admin_id,
                        f"💰 Новая продажа!\n"
                        f"Пользователь: @{message.from_user.username} ({message.from_user.id})\n"
                        f"Тариф: {VPN_PLANS[plan_id]['name']}\n"
                        f"Email: {email}\n"
                        f"Выдан ключ ID: {key_row['id']}"
                    )
                except:
                    pass
        else:
            await message.answer(
                "❌ Произошла ошибка при выдаче ключа. Администраторы уже уведомлены.",
                reply_markup=get_main_keyboard()
            )
            
            # Уведомление админам о проблеме
            for admin_id in ADMIN_IDS:
                try:
                    await bot.send_message(
                        admin_id,
                        f"⚠️ Проблема с выдачей ключа!\n"
                        f"Пользователь: {message.from_user.id}\n"
                        f"Тариф: {VPN_PLANS[plan_id]['name']}\n"
                        f"Закончились ключи!"
                    )
                except:
                    pass

@dp.message(Command("my_key"))
async def cmd_my_key(message: Message):
    """Проверка статуса подписки"""
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT vk.key_value, vk.duration_days, u.subscription_end
            FROM vpn_keys vk
            JOIN users u ON vk.assigned_to = u.user_id
            WHERE u.user_id = ? AND vk.is_used = 1
            ORDER BY vk.id DESC LIMIT 1
        ''', (message.from_user.id,))
        
        result = cursor.fetchone()
        
        if result:
            sub_end = datetime.fromisoformat(result['subscription_end'])
            days_left = (sub_end - datetime.now()).days
            
            if days_left > 0:
                await message.answer(
                    f"✅ <b>Ваша подписка активна</b>\n\n"
                    f"🔑 Ключ: <code>{result['key_value']}</code>\n"
                    f"📅 Действует до: {sub_end.strftime('%d.%m.%Y')}\n"
                    f"⏳ Осталось дней: {days_left}"
                )
            else:
                await message.answer(
                    "⚠️ Ваша подписка истекла. Приобретите новую в разделе VPN."
                )
        else:
            await message.answer(
                "У вас нет активной подписки. Приобретите её в разделе VPN-сервисы."
            )

async def main():
    # Инициализация БД
    init_db()
    
    # Проверяем наличие ключей в БД
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM vpn_keys WHERE is_used = 0')
        free_keys = cursor.fetchone()[0]
        if free_keys == 0:
            logger.warning(
                "В базе нет свободных ключей! "
                "Добавьте их через команду /add_keys ДНИ KEY1,KEY2,..."
            )
        else:
            logger.info(f"Свободных ключей в базе: {free_keys}")
    
    logger.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен пользователем")
