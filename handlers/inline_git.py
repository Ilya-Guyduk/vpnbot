"""
Инлайн-режим: git search / git pull

  @bot git search <запрос>          — поиск репозиториев
  @bot git pull <name или owner/repo> — список релизов → скачать выбранный

Фишки:
  - owner/ не обязателен: "git pull django" найдёт django/django сам
  - Показывает до 5 последних релизов, каждый — отдельный результат
  - Для каждого релиза перечислены все assets со ссылками
  - Если релизов нет — предлагает исходники (zip ветки)
  - Если файл > 45 МБ — даёт прямую ссылку вместо вложения
"""

import logging
import hashlib
from datetime import datetime

from aiogram import Router, F
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InlineQueryResultDocument,
    InputTextMessageContent,
    LinkPreviewOptions,
)

from services.github import search_repos, find_repo, get_releases, GHRelease, GHRepo

logger = logging.getLogger(__name__)
router = Router()

_MAX_MB     = 45
_NO_PREVIEW = LinkPreviewOptions(is_disabled=True)
_GH_THUMB   = "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png"


# ── маленькие хелперы ─────────────────────────────────────────────────────────

def _uid(*parts) -> str:
    return hashlib.md5("|".join(map(str, parts)).encode()).hexdigest()[:16]

def _stars(n: int) -> str:
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)

def _lang(lang: str | None) -> str:
    return f"[{lang}] " if lang else ""

def _date(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%d.%m.%Y")
    except Exception:
        return iso[:10]


# ── пустой запрос ─────────────────────────────────────────────────────────────

@router.inline_query(F.query == "")
async def inline_empty(query: InlineQuery) -> None:
    help_text = (
        "🖥 <b>Big Black Robot — Git-интерфейс</b>\n\n"
        "Команды:\n\n"
        "<code>git search django</code> — найти репозитории\n"
        "<code>git pull django</code> — релизы django/django\n"
        "<code>git pull psf/requests</code> — релизы конкретного репо\n\n"
        "owner/ писать необязательно — бот найдёт сам."
    )
    await query.answer(
        results=[
            InlineQueryResultArticle(
                id="help",
                title="🖥 Big Black Robot · Git",
                description="git search <запрос>  |  git pull <name или owner/repo>",
                input_message_content=InputTextMessageContent(message_text=help_text),
                thumbnail_url=_GH_THUMB,
            )
        ],
        cache_time=60,
        is_personal=False,
    )


# ── git search ────────────────────────────────────────────────────────────────

@router.inline_query(F.query.lower().startswith("git search "))
async def inline_git_search(query: InlineQuery) -> None:
    term = query.query[len("git search "):].strip()
    if not term:
        await query.answer([], cache_time=0)
        return

    repos = await search_repos(term, per_page=5)

    if not repos:
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    id="noresult",
                    title="❌ Ничего не найдено",
                    description=f"По запросу «{term}» репозиториев нет",
                    input_message_content=InputTextMessageContent(
                        message_text=f"🔍 По запросу <code>{term}</code> ничего не найдено."
                    ),
                )
            ],
            cache_time=30,
        )
        return

    results = []
    for repo in repos:
        topics = "  ".join(f"#{t}" for t in repo.topics[:3])
        text = (
            f'📦 <b><a href="{repo.html_url}">{repo.full_name}</a></b>\n\n'
            f"{repo.description}\n\n"
            f"⭐ {_stars(repo.stars)}   {_lang(repo.language)}💾 {repo.size_mb} MB"
            + (f"\n\n{topics}" if topics else "")
        )
        results.append(
            InlineQueryResultArticle(
                id=_uid("s", repo.full_name),
                title=f"{repo.full_name}  ⭐{_stars(repo.stars)}",
                description=f"{_lang(repo.language)}{repo.description[:90]}",
                input_message_content=InputTextMessageContent(
                    message_text=text,
                    link_preview_options=_NO_PREVIEW,
                ),
                thumbnail_url=_GH_THUMB,
            )
        )

    await query.answer(results, cache_time=30, is_personal=False)


# ── git pull ──────────────────────────────────────────────────────────────────

@router.inline_query(F.query.lower().startswith("git pull "))
async def inline_git_pull(query: InlineQuery) -> None:
    raw = query.query[len("git pull "):].strip()

    if not raw:
        await query.answer([], cache_time=0)
        return

    # Найти репо (owner/repo или поиск по имени)
    repo = await find_repo(raw)

    if not repo:
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    id="not_found",
                    title=f"❌ «{raw}» — не найдено",
                    description="Попробуй уточнить запрос или добавить owner/",
                    input_message_content=InputTextMessageContent(
                        message_text=f"❌ Репозиторий <code>{raw}</code> не найден."
                    ),
                )
            ],
            cache_time=10,
        )
        return

    releases = await get_releases(repo.full_name, per_page=6)

    # Нет релизов → предложить исходники
    if not releases:
        return await _answer_no_releases(query, repo)

    results = []
    for rel in releases:
        results.extend(_release_to_results(repo, rel))

    if not results:
        return await _answer_no_releases(query, repo)

    await query.answer(results[:20], cache_time=60, is_personal=False)


# ── Сборка результатов из одного релиза ──────────────────────────────────────

def _release_to_results(repo: GHRepo, rel: GHRelease) -> list:
    """
    Возвращает список InlineQueryResult для одного релиза.
    - Если есть assets — каждый asset отдельным результатом (Document или Article).
    - Если assets нет — одна карточка со ссылкой на zipball.
    """
    results = []
    tag     = rel.tag_name
    date    = _date(rel.published_at)
    label   = rel.label               # "(pre-release)" или ""
    notes   = rel.body[:300] + ("…" if len(rel.body) > 300 else "")

    def _base_caption() -> str:
        return (
            f'📦 <b><a href="{repo.html_url}/releases/tag/{tag}">'
            f"{repo.full_name} {tag}</a></b>{label}\n"
            f"📅 {date}\n\n"
            + (f"{notes}\n\n" if notes else "")
        )

    if not rel.assets:
        # Только исходники через zipball
        caption = _base_caption() + f"📥 <a href=\"{rel.zipball_url}\">Исходники (zip)</a>"
        results.append(
            InlineQueryResultArticle(
                id=_uid("rel", repo.full_name, tag, "src"),
                title=f"📦 {repo.name}  {tag}{label}  [{date}]",
                description="Исходный код (нет бинарных релизов)",
                input_message_content=InputTextMessageContent(
                    message_text=caption,
                    link_preview_options=_NO_PREVIEW,
                ),
                thumbnail_url=_GH_THUMB,
            )
        )
        return results

    for asset in rel.assets:
        asset_id  = _uid("asset", repo.full_name, tag, asset.name)
        size_str  = f"{asset.size_mb} MB"
        full_title = f"{tag}{label}  ·  {asset.name}  [{size_str}]"

        if asset.size_mb <= _MAX_MB:
            # Отправляем как вложение прямо в чат
            results.append(
                InlineQueryResultDocument(
                    id=asset_id,
                    title=f"⬇️ {full_title}",
                    description=f"{repo.full_name}  ·  {date}",
                    document_url=asset.download_url,
                    mime_type=asset.content_type,
                    caption=_base_caption() + f"📄 <b>{asset.name}</b>  {size_str}",
                )
            )
        else:
            # Слишком большой — карточка со ссылкой
            text = (
                _base_caption()
                + f"⚠️ <b>{asset.name}</b> ({size_str}) — слишком большой для Telegram.\n"
                f'📥 <a href="{asset.download_url}">Скачать напрямую</a>'
            )
            results.append(
                InlineQueryResultArticle(
                    id=asset_id,
                    title=f"🔗 {full_title}  [ссылка]",
                    description=f"Файл > {_MAX_MB} MB — будет ссылка вместо вложения",
                    input_message_content=InputTextMessageContent(
                        message_text=text,
                        link_preview_options=_NO_PREVIEW,
                    ),
                    thumbnail_url=_GH_THUMB,
                )
            )

    return results


# ── Fallback: репо без релизов ────────────────────────────────────────────────

async def _answer_no_releases(query: InlineQuery, repo: GHRepo) -> None:
    if repo.size_mb <= _MAX_MB:
        caption = (
            f'📦 <b><a href="{repo.html_url}">{repo.full_name}</a></b>\n'
            f"{repo.description}\n\n"
            f"⭐ {_stars(repo.stars)}   {_lang(repo.language)}💾 {repo.size_mb} MB\n"
            f"🌿 ветка: <code>{repo.default_branch}</code>\n\n"
            "⚠️ Официальных релизов нет — архив ветки по умолчанию."
        )
        await query.answer(
            results=[
                InlineQueryResultDocument(
                    id=_uid("src", repo.full_name),
                    title=f"⬇️ {repo.full_name}  [исходники, {repo.size_mb} MB]",
                    description="Релизов нет — архив основной ветки",
                    document_url=repo.source_zip_url,
                    mime_type="application/zip",
                    caption=caption,
                )
            ],
            cache_time=120,
            is_personal=False,
        )
    else:
        zip_url = f"{repo.html_url}/archive/refs/heads/{repo.default_branch}.zip"
        text = (
            f"⚠️ <b>{repo.full_name}</b> не имеет релизов.\n"
            f"Исходники ({repo.size_mb} MB) — слишком большие для Telegram.\n\n"
            f"📥 <a href=\"{zip_url}\">Скачать вручную</a>"
        )
        await query.answer(
            results=[
                InlineQueryResultArticle(
                    id=_uid("src_big", repo.full_name),
                    title=f"🔗 {repo.full_name}  — ссылка на исходники",
                    description=f"Нет релизов, {repo.size_mb} MB — даём ссылку",
                    input_message_content=InputTextMessageContent(
                        message_text=text,
                        link_preview_options=_NO_PREVIEW,
                    ),
                    thumbnail_url=_GH_THUMB,
                )
            ],
            cache_time=60,
        )