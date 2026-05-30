"""
База данных VPN-клиентов.
Структура: id → {name, platforms, protocols, description, versions}

platforms: список платформ из ICONS
versions:  {platform: {label, url, note?}}
"""

ICONS = {
    "android": "📱",
    "ios":     "🍎",
    "windows": "💻",
    "macos":   "🖥",
    "linux":   "🐧",
}

VPN_CLIENTS: dict[str, dict] = {

    "hiddify": {
        "name": "Hiddify",
        "platforms": ["android", "ios", "windows", "macos", "linux"],
        "protocols": ["VLESS", "Reality", "VMess", "Hysteria2", "Shadowsocks", "Trojan"],
        "description": (
            "Универсальный клиент с автовыбором лучшего протокола.\n"
            "Минималистичный интерфейс — настраивается одной ссылкой-подпиской.\n\n"
            "Рекомендуем как основной клиент."
        ),
        "versions": {
            "android": {
                "label": "Android  (Google Play / APK)",
                "url":   "https://github.com/hiddify/hiddify-app/releases/latest",
                "note":  "Минимум Android 5.0",
            },
            "ios": {
                "label": "iOS / iPadOS  (App Store)",
                "url":   "https://apps.apple.com/app/hiddify-proxy-vpn/id6596777532",
                "note":  "Требует Apple ID не из РФ",
            },
            "windows": {
                "label": "Windows  (.exe установщик)",
                "url":   "https://github.com/hiddify/hiddify-app/releases/latest",
                "note":  "Windows 10/11 x64",
            },
            "macos": {
                "label": "macOS  (.dmg)",
                "url":   "https://github.com/hiddify/hiddify-app/releases/latest",
                "note":  "macOS 12+, Intel и Apple Silicon",
            },
            "linux": {
                "label": "Linux  (.deb / .rpm / AppImage)",
                "url":   "https://github.com/hiddify/hiddify-app/releases/latest",
                "note":  "Ubuntu 20.04+, Fedora 36+",
            },
        },
    },

    "v2rayng": {
        "name": "v2rayNG",
        "platforms": ["android"],
        "protocols": ["VLESS", "VMess", "Shadowsocks", "Trojan", "SOCKS"],
        "description": (
            "Классика для Android. Лёгкий, стабильный, проверенный годами.\n"
            "Поддерживает импорт конфига по QR-коду и ссылке."
        ),
        "versions": {
            "android": {
                "label": "Android  (APK / Google Play)",
                "url":   "https://github.com/2dust/v2rayNG/releases/latest",
                "note":  "Android 5.0+, ARM / x86",
            },
        },
    },

    "v2rayn": {
        "name": "v2rayN",
        "platforms": ["windows"],
        "protocols": ["VLESS", "VMess", "Reality", "Shadowsocks", "Trojan", "SOCKS"],
        "description": (
            "Флагман для Windows. Богатый интерфейс, встроенный роутинг,\n"
            "подписки, правила по доменам — всё из коробки."
        ),
        "versions": {
            "windows": {
                "label": "Windows  (.zip портатив или установщик)",
                "url":   "https://github.com/2dust/v2rayN/releases/latest",
                "note":  "Windows 10/11, .NET 8 обязателен",
            },
        },
    },

    "nekobox": {
        "name": "NekoBox",
        "platforms": ["android", "windows", "linux"],
        "protocols": ["VLESS", "VMess", "Reality", "Hysteria2", "Shadowsocks", "TUIC"],
        "description": (
            "Современный клиент на базе sing-box.\n"
            "Поддерживает самые новые протоколы и тонкую настройку маршрутизации.\n"
            "Для продвинутых пользователей."
        ),
        "versions": {
            "android": {
                "label": "Android  (APK)",
                "url":   "https://github.com/MatsuriDayo/NekoBoxForAndroid/releases/latest",
                "note":  "Android 7.0+",
            },
            "windows": {
                "label": "Windows  (.zip)",
                "url":   "https://github.com/MatsuriDayo/nekoray/releases/latest",
                "note":  "Windows 10/11 x64",
            },
            "linux": {
                "label": "Linux  (AppImage / .deb)",
                "url":   "https://github.com/MatsuriDayo/nekoray/releases/latest",
                "note":  "Ubuntu 20.04 / Debian 11+",
            },
        },
    },

    "outline": {
        "name": "Outline",
        "platforms": ["android", "ios", "windows", "macos", "linux"],
        "protocols": ["Shadowsocks"],
        "description": (
            "Проект Google Jigsaw. Максимально простой — один ключ, все устройства.\n"
            "Идеален если нужно просто работать без лишних настроек."
        ),
        "versions": {
            "android": {
                "label": "Android  (Google Play / APK)",
                "url":   "https://play.google.com/store/apps/details?id=org.outline.android.client",
            },
            "ios": {
                "label": "iOS  (App Store)",
                "url":   "https://apps.apple.com/app/outline-app/id1356177741",
            },
            "windows": {
                "label": "Windows  (.exe)",
                "url":   "https://github.com/Jigsaw-Code/outline-apps/releases/latest",
                "note":  "Windows 10+",
            },
            "macos": {
                "label": "macOS  (App Store / .dmg)",
                "url":   "https://apps.apple.com/app/outline-secure-internet-access/id1356178125",
            },
            "linux": {
                "label": "Linux  (AppImage)",
                "url":   "https://github.com/Jigsaw-Code/outline-apps/releases/latest",
            },
        },
    },

    "wireguard": {
        "name": "WireGuard",
        "platforms": ["android", "ios", "windows", "macos", "linux"],
        "protocols": ["WireGuard"],
        "description": (
            "Официальный клиент WireGuard — быстрый и лёгкий VPN-протокол.\n"
            "Нужен WireGuard-конфиг от сервера. Хорош для корпоративных и личных серверов."
        ),
        "versions": {
            "android": {
                "label": "Android  (Google Play)",
                "url":   "https://play.google.com/store/apps/details?id=com.wireguard.android",
            },
            "ios": {
                "label": "iOS  (App Store)",
                "url":   "https://apps.apple.com/app/wireguard/id1441195209",
            },
            "windows": {
                "label": "Windows  (.msi установщик)",
                "url":   "https://download.wireguard.com/windows-client/wireguard-installer.exe",
                "note":  "Windows 10/11",
            },
            "macos": {
                "label": "macOS  (App Store)",
                "url":   "https://apps.apple.com/app/wireguard/id1451685025",
            },
            "linux": {
                "label": "Linux  (пакетный менеджер)",
                "url":   "https://www.wireguard.com/install/",
                "note":  "apt install wireguard / dnf install wireguard-tools",
            },
        },
    },
}