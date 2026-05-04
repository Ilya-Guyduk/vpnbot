"""
Скрипт для создания/обновления статей на Telegraph.

Использование:
    python create_articles.py

Создаёт все статьи и выводит их URL. URL нужно вставить в main.py
в словарь ARTICLES.

Для редактирования созданных статей используйте auth_url, который
вы получили при создании Telegraph-аккаунта.
"""

import asyncio
import os
import json
import aiohttp
from dotenv import load_dotenv

load_dotenv()

TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")

if not TELEGRAPH_TOKEN:
    raise ValueError("TELEGRAPH_TOKEN не задан в .env!")


# ============================================================
# ХЕЛПЕРЫ ДЛЯ ФОРМИРОВАНИЯ TELEGRAPH-КОНТЕНТА
# ============================================================
# Telegraph принимает контент в виде дерева Node-объектов.
# Каждый Node — это либо строка, либо dict с tag/children.
# Поддерживаемые теги: a, aside, b, blockquote, br, code, em,
# figure, h3, h4, hr, i, iframe, img, li, ol, p, pre, s,
# strong, u, ul, video.

def p(*children):
    """Параграф."""
    return {"tag": "p", "children": list(children)}

def h3(text):
    """Заголовок уровня 3 (большой)."""
    return {"tag": "h3", "children": [text]}

def h4(text):
    """Заголовок уровня 4 (поменьше)."""
    return {"tag": "h4", "children": [text]}

def b(text):
    """Жирный."""
    return {"tag": "strong", "children": [text]}

def i(text):
    """Курсив."""
    return {"tag": "em", "children": [text]}

def code(text):
    """Моноширинный (для команд, кода)."""
    return {"tag": "code", "children": [text]}

def link(text, url):
    """Ссылка."""
    return {"tag": "a", "attrs": {"href": url}, "children": [text]}

def anchor(text, heading):
    """
    Якорная ссылка на заголовок внутри той же статьи.
    heading — точный текст заголовка (h3/h4).
    Telegraph сам генерирует id из текста заголовка.
    """
    # Telegraph превращает текст заголовка в id: пробелы → дефисы,
    # сохраняет регистр и большинство символов как есть
    anchor_id = heading.replace(" ", "-")
    return {"tag": "a", "attrs": {"href": f"#{anchor_id}"}, "children": [text]}

def anchor(text, heading):
    """
    Якорная ссылка на заголовок внутри той же статьи.
    Telegraph автоматически создаёт ID для заголовков:
    пробелы заменяет на дефисы, спецсимволы убирает.
    """
    # Преобразуем заголовок в формат якоря
    anchor_id = heading.replace(" ", "-")
    return {"tag": "a", "attrs": {"href": f"#{anchor_id}"}, "children": [text]}

def ul(*items):
    """Маркированный список. items — список текстов или Node."""
    return {
        "tag": "ul",
        "children": [
            {"tag": "li", "children": [item] if isinstance(item, str) else item if isinstance(item, list) else [item]}
            for item in items
        ]
    }

def ol(*items):
    """Нумерованный список."""
    return {
        "tag": "ol",
        "children": [
            {"tag": "li", "children": [item] if isinstance(item, str) else item if isinstance(item, list) else [item]}
            for item in items
        ]
    }

def li(*children):
    """Элемент списка с несколькими детьми."""
    return list(children)

def blockquote(*children):
    """Цитата (для важных предупреждений)."""
    return {"tag": "blockquote", "children": list(children)}

def hr():
    """Горизонтальная черта."""
    return {"tag": "hr"}


# ============================================================
# СТАТЬЯ: ANDROID
# ============================================================

ANDROID_ARTICLE = {
    "title": "Подключение VPN на Android",
    "author_name": "VPN Bot",
    "content": [
        p("Ниже — подробная инструкция по подключению нашего VPN на Android. Используется протокол ", b("VLESS Reality"), " — один из самых стабильных способов обхода блокировок в России на сегодня."),

        h3("Содержание"),
        ul(
            anchor("Какое приложение выбрать", "Какое-приложение-выбрать"),
            anchor("Способ 1 — v2rayNG", "Способ-1-—-v2rayNG"),
            anchor("Способ 2 — Hiddify", "Способ-2-—-Hiddify"),
            anchor("Решение проблем", "Решение-проблем"),
            anchor("Полезные мелочи", "Полезные-мелочи"),
        ),

        hr(),

        h3("Какое приложение выбрать"),

        p("Для VLESS Reality нужен специальный клиент. Рекомендуем по порядку:"),

        ul(
            li(b("v2rayNG"), " — самый популярный, стабильный, активно обновляется"),
            li(b("Hiddify"), " — современный интерфейс, проще для новичков"),
            li(b("NekoBox"), " — мощный, для продвинутых пользователей"),
        ),

        blockquote(
            p(b("Важно: "), "В Google Play эти приложения периодически скрывают для российских аккаунтов. Если в Play Маркет их нет — устанавливайте APK с GitHub (ссылки ниже). Это безопасно — это официальные релизы от разработчиков.")
        ),

        hr(),

        h3("Способ 1 — v2rayNG"),

        h4("Шаг 1. Установите приложение"),

        p("Откройте на телефоне страницу релизов:"),
        p(link("github.com/2dust/v2rayNG/releases", "https://github.com/2dust/v2rayNG/releases")),

        p("Скачайте файл с названием вида ", code("v2rayNG_X.X.X_universal.apk"), " (последняя версия)."),

        p("Откройте скачанный APK — Android попросит разрешить установку из неизвестных источников. Разрешите для браузера или файлового менеджера."),

        h4("Шаг 2. Импортируйте ключ"),

        p("После покупки бот пришлёт вам два варианта:"),
        ul(
            "QR-код (картинка)",
            "Текстовая ссылка вида vless://..."
        ),

        p(b("Если у вас QR-код:")),
        ol(
            "Откройте v2rayNG",
            "Нажмите «+» в правом верхнем углу",
            "Выберите «Импорт конфигурации из QR-кода»",
            "Отсканируйте QR с экрана компьютера или другого устройства"
        ),

        p(b("Если у вас текстовая ссылка:")),
        ol(
            "Скопируйте ссылку из бота (долгое нажатие → копировать)",
            "Откройте v2rayNG",
            "Нажмите «+» → «Импорт конфигурации из буфера обмена»",
            "Конфиг добавится автоматически"
        ),

        h4("Шаг 3. Подключитесь"),

        ol(
            "В списке профилей нажмите на добавленный сервер",
            "Нажмите большую круглую кнопку «V» внизу справа",
            "Android спросит разрешение на VPN — согласитесь",
            "Кнопка станет зелёной — VPN подключён"
        ),

        h4("Шаг 4. Проверьте работу"),

        p("Откройте сайт ", link("2ip.ru", "https://2ip.ru"), " — он должен показать другой IP-адрес и страну."),

        hr(),

        h3("Способ 2 — Hiddify"),

        p("Если интерфейс v2rayNG показался сложным — попробуйте Hiddify. Он более дружелюбен к новичкам."),

        p(b("Установка:"), " ", link("github.com/hiddify/hiddify-app/releases", "https://github.com/hiddify/hiddify-app/releases"), " — скачайте файл с пометкой Android."),

        p(b("Подключение:")),
        ol(
            "Откройте Hiddify",
            "Нажмите «Добавить профиль»",
            "Выберите «Импорт из буфера обмена» или сканер QR-кода",
            "Нажмите «Подключиться»"
        ),

        hr(),

        h3("Решение проблем"),

        h4("VPN подключается, но интернет не работает"),

        p("Проверьте по очереди:"),
        ul(
            "Корректность ключа — попробуйте удалить профиль и импортировать заново",
            "Срок действия подписки в боте — команда /my_key",
            "Перезагрузите телефон и попробуйте снова",
            "Попробуйте другой клиент (если был v2rayNG — поставьте Hiddify, и наоборот)"
        ),

        h4("Не получается установить APK"),

        p("Откройте ", b("Настройки → Приложения → Специальный доступ → Установка неизвестных приложений"), ". Найдите браузер или файловый менеджер, через который пытаетесь установить, и разрешите."),

        h4("Подключается, но некоторые сайты не открываются"),

        p("Иногда помогает смена DNS внутри клиента. В v2rayNG откройте Настройки → Удалённый DNS → впишите ", code("1.1.1.1"), " или ", code("8.8.8.8"), "."),

        hr(),

        h3("Полезные мелочи"),

        ul(
            "В v2rayNG можно настроить автоподключение при старте телефона: Настройки → Опции по умолчанию → «Автоматически подключаться при старте»",
            "Чтобы VPN работал только для отдельных приложений, включите режим «Per-app proxy» в настройках",
            "На Android TV v2rayNG тоже работает, но иконку приходится запускать через файловый менеджер",
        ),

        p(i("Если что-то не получилось — напишите в поддержку через меню «Помощь» в боте.")),
    ]
}


# ============================================================
# ВЫЗОВ TELEGRAPH API
# ============================================================

async def create_page(session, title, content, author_name="VPN Bot"):
    """Создать новую страницу на Telegraph."""
    url = "https://api.telegra.ph/createPage"
    data = {
        "access_token": TELEGRAPH_TOKEN,
        "title": title,
        "author_name": author_name,
        "content": json.dumps(content, ensure_ascii=False),
        "return_content": "false"
    }
    async with session.post(url, data=data) as resp:
        result = await resp.json()
        if not result.get("ok"):
            raise Exception(f"Telegraph error: {result}")
        return result["result"]


async def edit_page(session, path, title, content, author_name="VPN Bot"):
    """
    Обновить существующую страницу по path (часть URL после telegra.ph/).
    Например, для https://telegra.ph/Podklyuchenie-VPN-na-Android-05-04-2
    path будет 'Podklyuchenie-VPN-na-Android-05-04-2'.
    """
    url = "https://api.telegra.ph/editPage"
    data = {
        "access_token": TELEGRAPH_TOKEN,
        "path": path,
        "title": title,
        "author_name": author_name,
        "content": json.dumps(content, ensure_ascii=False),
        "return_content": "false"
    }
    async with session.post(url, data=data) as resp:
        result = await resp.json()
        if not result.get("ok"):
            raise Exception(f"Telegraph error: {result}")
        return result["result"]


def url_to_path(url):
    """Извлекает path из URL Telegraph."""
    return url.rstrip("/").split("/")[-1]


# ============================================================
# СУЩЕСТВУЮЩИЕ СТАТЬИ
# ============================================================
# Если статья уже создана — впиши её URL сюда, и скрипт будет
# её обновлять, а не создавать новую.

EXISTING_ARTICLES = {
    "android": "https://telegra.ph/Podklyuchenie-VPN-na-Android-05-04-2",
    # "ios": "...",
    # "windows": "...",
    # "linux": "...",
}


async def main():
    articles_to_create = [
        ("android", ANDROID_ARTICLE),
        # Сюда позже добавим: ios, windows, linux, goodbyedpi, zapret, byebye_dpi, tor, dns
    ]

    print("=" * 60)
    print("СОЗДАНИЕ/ОБНОВЛЕНИЕ СТАТЕЙ НА TELEGRAPH")
    print("=" * 60)

    results = {}

    async with aiohttp.ClientSession() as session:
        for slug, article in articles_to_create:
            existing_url = EXISTING_ARTICLES.get(slug)
            
            try:
                if existing_url:
                    # Обновляем существующую статью
                    path = url_to_path(existing_url)
                    print(f"\n🔄 Обновляю статью: {slug} ({existing_url})")
                    page = await edit_page(
                        session,
                        path=path,
                        title=article["title"],
                        content=article["content"],
                        author_name=article.get("author_name", "VPN Bot")
                    )
                    results[slug] = page["url"]
                    print(f"   ✅ Обновлено: {page['url']}")
                else:
                    # Создаём новую
                    print(f"\n📝 Создаю статью: {slug}...")
                    page = await create_page(
                        session,
                        title=article["title"],
                        content=article["content"],
                        author_name=article.get("author_name", "VPN Bot")
                    )
                    results[slug] = page["url"]
                    print(f"   ✅ Создано: {page['url']}")
            except Exception as e:
                print(f"   ❌ Ошибка: {e}")

    print("\n" + "=" * 60)
    print("ГОТОВО! Актуальные URL статей:")
    print("=" * 60)
    print()
    print("ARTICLES = {")
    for slug, url in results.items():
        print(f'    "{slug}": "{url}",')
    print("}")
    print()
    print("=" * 60)
    print("ВАЖНО:")
    print("- Если URL изменился — обнови ARTICLES в main.py")
    print("- Чтобы редактировать через сайт — используй auth_url,")
    print("  который ты получил при создании Telegraph-аккаунта")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
