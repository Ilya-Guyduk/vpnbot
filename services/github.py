"""GitHub API wrapper: repos + releases."""

import logging
import aiohttp
from dataclasses import dataclass, field
from config import GITHUB_TOKEN

logger = logging.getLogger(__name__)

_API   = "https://api.github.com"
_CLOAD = "https://codeload.github.com"


def _headers() -> dict:
    h = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


async def _get(url: str, params: dict | None = None) -> dict | list | None:
    try:
        async with aiohttp.ClientSession() as s:
            async with s.get(
                url, headers=_headers(), params=params,
                timeout=aiohttp.ClientTimeout(total=8),
            ) as r:
                if r.status == 403:
                    logger.warning("GitHub rate limit exceeded")
                    return None
                if r.status == 404:
                    return None
                if r.status != 200:
                    logger.error("GitHub %s → status %s", url, r.status)
                    return None
                return await r.json()
    except Exception as e:
        logger.exception("GitHub request error: %s", e)
        return None


# ── Repo ──────────────────────────────────────────────────────────────────────

@dataclass
class GHRepo:
    full_name:      str
    name:           str
    description:    str
    stars:          int
    language:       str | None
    default_branch: str
    size_kb:        int
    html_url:       str
    topics:         list[str]

    @property
    def size_mb(self) -> float:
        return round(self.size_kb / 1024, 1)

    @property
    def source_zip_url(self) -> str:
        return f"{_CLOAD}/{self.full_name}/zip/refs/heads/{self.default_branch}"


def _parse_repo(d: dict) -> GHRepo:
    return GHRepo(
        full_name=d["full_name"],
        name=d["name"],
        description=d.get("description") or "Без описания",
        stars=d.get("stargazers_count", 0),
        language=d.get("language"),
        default_branch=d.get("default_branch", "main"),
        size_kb=d.get("size", 0),
        html_url=d["html_url"],
        topics=d.get("topics", []),
    )


async def search_repos(query: str, per_page: int = 5) -> list[GHRepo]:
    data = await _get(f"{_API}/search/repositories",
                      {"q": query, "sort": "stars", "order": "desc", "per_page": per_page})
    if not data:
        return []
    return [_parse_repo(item) for item in data.get("items", [])]


async def get_repo(owner_repo: str) -> GHRepo | None:
    owner_repo = owner_repo.strip().strip("/")
    if "/" not in owner_repo:
        return None
    data = await _get(f"{_API}/repos/{owner_repo}")
    return _parse_repo(data) if data else None


async def find_repo(query: str) -> GHRepo | None:
    """owner/repo → прямой запрос. Иначе — поиск, топ-1 по звёздам."""
    if "/" in query:
        return await get_repo(query)
    repos = await search_repos(query, per_page=1)
    return repos[0] if repos else None


# ── Release ───────────────────────────────────────────────────────────────────

@dataclass
class GHAsset:
    name:         str
    download_url: str
    size_bytes:   int
    content_type: str

    @property
    def size_mb(self) -> float:
        return round(self.size_bytes / 1024 / 1024, 1)

    @property
    def is_source(self) -> bool:
        return self.name.endswith((".zip", ".tar.gz", ".tgz"))


@dataclass
class GHRelease:
    tag_name:      str
    name:          str
    published_at:  str           # ISO 8601
    body:          str           # release notes
    assets:        list[GHAsset]
    zipball_url:   str           # исходники (fallback)
    prerelease:    bool
    draft:         bool
    repo_full_name: str = ""

    @property
    def date_short(self) -> str:
        return self.published_at[:10] if self.published_at else "?"

    @property
    def label(self) -> str:
        flags = []
        if self.prerelease:
            flags.append("pre-release")
        if self.draft:
            flags.append("draft")
        return f" ({', '.join(flags)})" if flags else ""


def _parse_release(d: dict, repo_full_name: str = "") -> GHRelease:
    assets = [
        GHAsset(
            name=a["name"],
            download_url=a["browser_download_url"],
            size_bytes=a.get("size", 0),
            content_type=a.get("content_type", "application/octet-stream"),
        )
        for a in d.get("assets", [])
    ]
    return GHRelease(
        tag_name=d["tag_name"],
        name=d.get("name") or d["tag_name"],
        published_at=d.get("published_at", ""),
        body=(d.get("body") or "").strip(),
        assets=assets,
        zipball_url=d.get("zipball_url", ""),
        prerelease=d.get("prerelease", False),
        draft=d.get("draft", False),
        repo_full_name=repo_full_name,
    )


async def get_releases(owner_repo: str, per_page: int = 6) -> list[GHRelease]:
    """Получить список релизов (без draft, отсортированы по дате убыв.)."""
    data = await _get(f"{_API}/repos/{owner_repo}/releases",
                      {"per_page": per_page})
    if not isinstance(data, list):
        return []
    return [
        _parse_release(r, owner_repo)
        for r in data
        if not r.get("draft")
    ]