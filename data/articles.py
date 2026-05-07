"""
Ссылки на статьи Telegraph.
Создаются скриптом create_articles.py, редактируются через auth_url в браузере.
"""

ARTICLES: dict[str, str] = {
    "android":         "https://telegra.ph/Podklyuchenie-VPN-na-Android-05-04-2",
    "routing_v2rayng": "https://telegra.ph/Marshrutizaciya-v-v2rayNG--rossijskie-sajty-napryamuyu-05-05",
    # "ios":     "...",
    # "windows": "...",
    # "linux":   "...",
}

PLATFORM_NAMES: dict[str, str] = {
    "android": "Android",
    "ios":     "iOS",
    "windows": "Windows",
    "linux":   "Linux",
}
