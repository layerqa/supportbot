from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.chat_type import ChatTypeFilter
from app.i18n import SUPPORTED_LOCALES, resolve_locale, t
from app.services.users import get_or_create_user, set_locale

router = Router(name="language")
router.message.filter(ChatTypeFilter("private"))

_LOCALE_LABELS = {"ru": "🇷🇺 Русский", "en": "🇬🇧 English"}


def _language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=_LOCALE_LABELS[code], callback_data=f"set_locale:{code}"
                )
                for code in SUPPORTED_LOCALES
            ]
        ]
    )


@router.message(Command("language"))
async def cmd_language(message: Message, session: AsyncSession) -> None:
    tg_user = message.from_user
    user = await get_or_create_user(
        session,
        telegram_id=tg_user.id,
        full_name=tg_user.full_name,
        username=tg_user.username,
    )
    locale = resolve_locale(user.locale or tg_user.language_code)
    await message.answer(t(locale, "language_prompt"), reply_markup=_language_keyboard())
    await session.commit()


@router.callback_query(F.data.startswith("set_locale:"))
async def on_set_locale(callback: CallbackQuery, session: AsyncSession) -> None:
    locale = resolve_locale(callback.data.split(":", 1)[1])
    tg_user = callback.from_user
    user = await get_or_create_user(
        session,
        telegram_id=tg_user.id,
        full_name=tg_user.full_name,
        username=tg_user.username,
    )
    await set_locale(session, user, locale)
    await session.commit()

    await callback.message.edit_text(t(locale, "language_set"))
    await callback.answer()
