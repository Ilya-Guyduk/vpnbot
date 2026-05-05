"""
Скрипт для создания/обновления статей на Telegraph из Markdown-файлов.

Использование:
    python create_articles.py              # Все статьи
    python create_articles.py android      # Только указанная статья

Статьи лежат в папке articles/ в формате .md.
Список URL и метаданных — в articles/_config.py.

Чтобы добавить новую статью:
1. Создай articles/имя.md
2. Добавь "имя": None в ARTICLES в articles/_config.py
3. Запусти скрипт — он создаст статью и выведет URL
4. Вставь URL вместо None в _config.py

Чтобы редактировать существующую статью:
1. Правь .md файл
2. Запусти скрипт — статья обновится по сохранённому URL
"""

import asyncio
import json
import os
import re
import sys
from pathlib import Path

import aiohttp
from dotenv import load_dotenv

# Импорт конфига статей
sys.path.insert(0, str(Path(__file__).parent / "articles"))
from articles._config import ARTICLES, DEFAULT_AUTHOR  # noqa: E402

load_dotenv()

TELEGRAPH_TOKEN = os.getenv("TELEGRAPH_TOKEN")
ARTICLES_DIR = Path(__file__).parent / "articles"

if not TELEGRAPH_TOKEN:
    raise ValueError("TELEGRAPH_TOKEN не задан в .env!")


# ============================================================
# КОНВЕРТЕР MARKDOWN -> TELEGRAPH NODES
# ============================================================
# Telegraph принимает контент как дерево узлов вида:
#   {"tag": "p", "children": ["текст", {"tag": "b", "children": ["жирный"]}]}
# Поддерживаемые теги: a, blockquote, br, code, em, h3, h4, hr,
# i, img, li, ol, p, pre, strong, ul.
#
# Это упрощённый парсер — поддерживает то, что нам реально нужно
# для гайдов: заголовки, списки, ссылки, жирный/курсив, код,
# цитаты, горизонтальные линии, абзацы.


def parse_inline(text):
    """
    Парсит inline-форматирование внутри строки текста:
    **жирный**, *курсив*, `код`, [текст](url)

    Возвращает список узлов Telegraph (строки и dict-ы).
    """
    nodes = []
    pos = 0

    # Регулярка ищет любой из паттернов, выбирает первое совпадение
    pattern = re.compile(
        r"(\*\*(?P<bold>[^*]+)\*\*)"           # **жирный**
        r"|(`(?P<code>[^`]+)`)"                # `код`
        r"|(\[(?P<link_text>[^\]]+)\]\((?P<link_url>[^)]+)\))"  # [текст](url)
        r"|(\*(?P<italic>[^*]+)\*)"            # *курсив*
    )

    for match in pattern.finditer(text):
        # Текст до совпадения — добавляем как есть
        if match.start() > pos:
            nodes.append(text[pos:match.start()])

        if match.group("bold"):
            nodes.append({"tag": "strong", "children": [match.group("bold")]})
        elif match.group("code"):
            nodes.append({"tag": "code", "children": [match.group("code")]})
        elif match.group("link_text"):
            nodes.append({
                "tag": "a",
                "attrs": {"href": match.group("link_url")},
                "children": [match.group("link_text")]
            })
        elif match.group("italic"):
            nodes.append({"tag": "em", "children": [match.group("italic")]})

        pos = match.end()

    # Хвост после последнего совпадения
    if pos < len(text):
        nodes.append(text[pos:])

    # Если ничего не нашли — возвращаем просто строку
    if not nodes:
        return [text]

    return nodes


def parse_markdown(markdown):
    """
    Парсит markdown-файл и возвращает (title, content_nodes).
    Title берётся из первого # заголовка.
    """
    lines = markdown.split("\n")
    title = ""
    nodes = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        # Заголовок верхнего уровня — это title статьи
        if line.startswith("# ") and not title:
            title = line[2:].strip()
            i += 1
            continue

        # Заголовки h3 (### Foo) и h4 (#### Foo)
        if line.startswith("#### "):
            nodes.append({"tag": "h4", "children": [line[5:].strip()]})
            i += 1
            continue
        if line.startswith("### "):
            nodes.append({"tag": "h3", "children": [line[4:].strip()]})
            i += 1
            continue

        # Горизонтальная линия
        if line.strip() == "---":
            nodes.append({"tag": "hr"})
            i += 1
            continue

        # Цитата (>)
        if line.startswith("> "):
            quote_lines = []
            while i < len(lines) and lines[i].startswith("> "):
                quote_lines.append(lines[i][2:].strip())
                i += 1
            quote_text = " ".join(quote_lines)
            nodes.append({
                "tag": "blockquote",
                "children": [{"tag": "p", "children": parse_inline(quote_text)}]
            })
            continue

        # Блок кода (```)
        if line.strip().startswith("```"):
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            i += 1  # Пропустить закрывающие ```
            code_text = "\n".join(code_lines)
            nodes.append({"tag": "pre", "children": [code_text]})
            continue

        # Маркированный список (- item) или нумерованный (1. item)
        if re.match(r"^\s*[-*]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
            is_ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            list_items = []
            while i < len(lines):
                current = lines[i]
                if re.match(r"^\s*[-*]\s+", current) or re.match(r"^\s*\d+\.\s+", current):
                    item_text = re.sub(r"^\s*([-*]|\d+\.)\s+", "", current).strip()
                    list_items.append({
                        "tag": "li",
                        "children": parse_inline(item_text)
                    })
                    i += 1
                elif current.strip() == "":
                    # Пустая строка — конец списка
                    break
                else:
                    break
            nodes.append({
                "tag": "ol" if is_ordered else "ul",
                "children": list_items
            })
            continue

        # Пустая строка — пропускаем
        if line.strip() == "":
            i += 1
            continue

        # Обычный абзац (может быть многострочным)
        para_lines = []
        while i < len(lines) and lines[i].strip() != "":
            current = lines[i].rstrip()
            # Проверим что строка не начинает другой блок
            if (current.startswith("#") or current.startswith(">") or
                current.startswith("```") or current.strip() == "---" or
                re.match(r"^\s*[-*]\s+", current) or
                re.match(r"^\s*\d+\.\s+", current)):
                break
            para_lines.append(current)
            i += 1

        if para_lines:
            para_text = " ".join(para_lines)
            nodes.append({"tag": "p", "children": parse_inline(para_text)})

    return title, nodes


# ============================================================
# ВЫЗОВ TELEGRAPH API
# ============================================================

async def create_page(session, title, content, author_name=DEFAULT_AUTHOR):
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


async def edit_page(session, path, title, content, author_name=DEFAULT_AUTHOR):
    """Обновить существующую страницу на Telegraph."""
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
    """Извлекает path из URL Telegraph (часть после telegra.ph/)."""
    return url.replace("https://telegra.ph/", "").replace("http://telegra.ph/", "").strip("/")


# ============================================================
# ОСНОВНАЯ ЛОГИКА
# ============================================================

async def process_article(session, slug):
    """Создать или обновить одну статью."""
    md_file = ARTICLES_DIR / f"{slug}.md"

    if not md_file.exists():
        print(f"   ❌ Файл не найден: {md_file}")
        return None

    markdown_text = md_file.read_text(encoding="utf-8")
    title, content = parse_markdown(markdown_text)

    if not title:
        print(f"   ❌ В файле нет заголовка # ...")
        return None

    existing_url = ARTICLES.get(slug)

    try:
        if existing_url:
            # Обновляем существующую
            print(f"🔄 Обновляю статью: {slug} ({existing_url})")
            path = url_to_path(existing_url)
            page = await edit_page(session, path, title, content)
            print(f"   ✅ Обновлено: {page['url']}")
            return page["url"]
        else:
            # Создаём новую
            print(f"🆕 Создаю новую статью: {slug}")
            page = await create_page(session, title, content)
            print(f"   ✅ Создано: {page['url']}")
            print(f"   ⚠️  ВАЖНО: добавь этот URL в articles/_config.py!")
            return page["url"]
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")
        return None


async def main():
    # Если передан аргумент — обрабатываем только одну статью
    target_slug = sys.argv[1] if len(sys.argv) > 1 else None

    print("=" * 60)
    print("СОЗДАНИЕ/ОБНОВЛЕНИЕ СТАТЕЙ НА TELEGRAPH")
    print("=" * 60)

    # Собираем список slug для обработки
    if target_slug:
        slugs = [target_slug]
        if target_slug not in ARTICLES:
            print(f"⚠️  Статьи '{target_slug}' нет в _config.py — будет создана новая")
    else:
        # Берём все .md файлы из папки articles, кроме служебных (с _ в начале)
        slugs = sorted(
            f.stem for f in ARTICLES_DIR.glob("*.md")
            if not f.stem.startswith("_")
        )

    results = {}

    async with aiohttp.ClientSession() as session:
        for slug in slugs:
            url = await process_article(session, slug)
            if url:
                results[slug] = url

    print()
    print("=" * 60)
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
    print("- Если создавалась новая статья — обнови URL в articles/_config.py")
    print("- Также обнови ARTICLES в main.py если используешь эту статью в боте")
    print("- Чтобы редактировать через сайт — используй auth_url,")
    print("  который ты получил при создании Telegraph-аккаунта")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
