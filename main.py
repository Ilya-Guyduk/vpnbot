import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, CRYPTO_BOT_TOKEN, MAIN_MENU_ENABLED, ADMIN_MENU_ENABLED, INLINE_MODE_ENABLED, XUI_API_URL, XUI_API_TOKEN
from services.xui_panel_api_client.xui_panel_api_client.client import AuthenticatedClient
from services.xui_panel_api_client.xui_panel_api_client.api.authentication import post_login

from database.db import init_db
from handlers import admin, inline_git, menu
from services.cryptobot import check_app
from services.poller import payment_poller

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    if MAIN_MENU_ENABLED:
        dp.include_router(menu.router)
    if ADMIN_MENU_ENABLED:
        dp.include_router(admin.router)
    if INLINE_MODE_ENABLED:
        dp.include_router(inline_git.router)
    return dp


async def main() -> None:
    xui_client = AuthenticatedClient(base_url=XUI_API_URL, token=XUI_API_TOKEN, verify_ssl=True)
    init_db()

    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    if CRYPTO_BOT_TOKEN:
        ok = await check_app()
        if ok:
            logger.info("CryptoBot: подключён ✓")
        else:
            logger.error("CryptoBot: токен невалиден — оплата не будет работать!")
    else:
        logger.warning("CryptoBot: токен не задан")

    dp = create_dispatcher()
    dp["xui_client"] = xui_client

    # Запускаем фоновый поллер платежей
    poller_task = asyncio.create_task(payment_poller(bot, xui_client))

    logger.info("Бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        poller_task.cancel()
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен пользователем")
