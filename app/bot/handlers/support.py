import html

from aiogram import Bot, Router
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.chat_type import ChatTypeFilter
from app.config import settings
from app.i18n import resolve_locale, t
from app.services.tickets import create_ticket, get_open_ticket
from app.services.users import get_or_create_user

router = Router(name="support")
router.message.filter(ChatTypeFilter("private"))


def _render_ticket_card(full_name: str, telegram_id: int, language_code: str | None) -> str:
    name = html.escape(full_name)
    lang = html.escape(language_code) if language_code else "—"
    return (
        f"🧑 <code>{name}</code>\n\n"
        f'🆔 <code>{telegram_id}</code> [<a href="tg://user?id={telegram_id}">open chat</a>]\n\n'
        f"<b>🌐 language_code:</b> {lang}"
    )


def _ban_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚫 Забанить", callback_data=f"ban:{telegram_id}")]
        ]
    )


@router.message()
async def relay_to_support(message: Message, bot: Bot, session: AsyncSession) -> None:
    tg_user = message.from_user
    user = await get_or_create_user(
        session,
        telegram_id=tg_user.id,
        full_name=tg_user.full_name,
        username=tg_user.username,
    )
    locale = resolve_locale(user.locale or tg_user.language_code)

    if user.is_banned:
        await message.answer(t(locale, "banned"))
        return

    ticket = await get_open_ticket(session, user)
    if ticket is None:
        topic = await bot.create_forum_topic(
            chat_id=settings.support_chat_id,
            name=f"{user.full_name} (id{user.telegram_id})",
        )
        ticket = await create_ticket(session, user, thread_id=topic.message_thread_id)

        await bot.send_message(
            chat_id=settings.support_chat_id,
            message_thread_id=ticket.thread_id,
            text=_render_ticket_card(user.full_name, user.telegram_id, tg_user.language_code),
            reply_markup=_ban_keyboard(user.telegram_id),
        )
        await message.answer(t(locale, "welcome", org=html.escape(settings.support_org_name)))

    await message.copy_to(
        chat_id=settings.support_chat_id,
        message_thread_id=ticket.thread_id,
    )
    await session.commit()
