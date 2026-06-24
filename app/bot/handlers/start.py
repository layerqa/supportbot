import html

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.chat_type import ChatTypeFilter
from app.config import settings
from app.i18n import resolve_locale, t
from app.services.users import get_or_create_user

router = Router(name="start")
router.message.filter(ChatTypeFilter("private"))


@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession) -> None:
    tg_user = message.from_user
    user, _ = await get_or_create_user(
        session,
        telegram_id=tg_user.id,
        full_name=tg_user.full_name,
        username=tg_user.username,
    )
    locale = resolve_locale(user.locale or tg_user.language_code)
    await message.answer(t(locale, "welcome", org=html.escape(settings.support_org_name)))
    await session.commit()


@router.message(Command("help"))
async def cmd_help(message: Message, session: AsyncSession) -> None:
    tg_user = message.from_user
    user, _ = await get_or_create_user(
        session,
        telegram_id=tg_user.id,
        full_name=tg_user.full_name,
        username=tg_user.username,
    )
    locale = resolve_locale(user.locale or tg_user.language_code)
    await message.answer(t(locale, "help"))
    await session.commit()
