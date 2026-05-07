"""Руководства по настройке VPN."""

from aiogram import Router, F
from aiogram import types
from aiogram.types import CallbackQuery

from data.articles import ARTICLES, PLATFORM_NAMES
from keyboards.inline import kb_guide

router = Router()


@router.callback_query(F.data.startswith("guide_"))
async def cb_guide(callback: CallbackQuery) -> None:
    platform = callback.data.removeprefix("guide_")
    name = PLATFORM_NAMES.get(platform, platform)
    url = ARTICLES.get(platform)

    if url:
        text = (
            f"📖 <b>Подключение VPN на {name}</b>\n\n"
            f"Подробное руководство со скриншотами и решением частых проблем:\n\n"
            f"👉 {url}\n\n"
            f"<i>Если что-то не получилось — напишите в раздел «Помощь».</i>"
        )
    else:
        text = (
            f"📖 <b>Руководство для {name}</b>\n\n"
            "🚧 Подробная инструкция в разработке.\n\n"
            "Воспользуйтесь руководством для другой платформы или "
            "напишите в раздел «Помощь» — поможем настроить вручную."
        )

    await callback.message.edit_text(
        text,
        reply_markup=kb_guide(platform, url),
        link_preview_options=types.LinkPreviewOptions(is_disabled=not url),
    )
    await callback.answer()
