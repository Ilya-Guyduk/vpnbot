"""
Конфиг со списком статей и их URL на Telegraph.

Если статья уже создана — указан её URL, и скрипт create_articles.py
будет её обновлять, а не создавать новую.

Если URL = None или ключа нет — будет создана новая статья.

После создания новой статьи нужно вписать её URL сюда вручную.
"""

# Slug (имя файла без .md) -> URL на Telegraph (или None если ещё не создана)
ARTICLES = {
    "android": "https://telegra.ph/Podklyuchenie-VPN-na-Android-05-04-2",
    "routing_v2rayng": "https://telegra.ph/Marshrutizaciya-v-v2rayNG--rossijskie-sajty-napryamuyu-05-05",
    # "ios": None,
    # "windows": None,
    # "linux": None,
}

# Имя автора по умолчанию для всех статей
DEFAULT_AUTHOR = "VPN Bot"
