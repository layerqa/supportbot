import html

from aiogram import Bot, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyParameters,
    User as TgUser,
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.chat_type import ChatTypeFilter
from app.config import settings
from app.db.models.ticket import Ticket
from app.db.models.user import User
from app.i18n import resolve_locale, t
from app.services.messages import find_group_message_id, record_relayed_message
from app.services.tickets import close_ticket, create_ticket, get_open_ticket
from app.services.users import get_or_create_user

router = Router(name="support")
router.message.filter(ChatTypeFilter("private"))


def _render_ticket_card(
    full_name: str,
    username: str | None,
    telegram_id: int,
    language_code: str | None,
    can_open_chat: bool,
) -> str:
    name = html.escape(full_name)
    username_text = f" (@{html.escape(username)})" if username else ""
    lang = html.escape(language_code) if language_code else "—"
    open_chat = (
        f' [<a href="tg://user?id={telegram_id}">open chat</a>]' if can_open_chat else ""
    )
    return (
        f"🧑 <code>{name}</code>{username_text}\n\n"
        f"🆔 <code>{telegram_id}</code>{open_chat}\n\n"
        f"<b>🌐 language_code:</b> {lang}"
    )


def _ban_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚫 Забанить", callback_data=f"ban:{telegram_id}")]
        ]
    )


async def _open_ticket(
    bot: Bot, session: AsyncSession, user: User, tg_user: TgUser
) -> Ticket:
    topic = await bot.create_forum_topic(
        chat_id=settings.support_chat_id,
        name=f"{user.full_name} (id{user.telegram_id})",
    )
    ticket = await create_ticket(session, user, thread_id=topic.message_thread_id)

    chat_info = await bot.get_chat(user.telegram_id)
    await bot.send_message(
        chat_id=settings.support_chat_id,
        message_thread_id=ticket.thread_id,
        text=_render_ticket_card(
            user.full_name,
            tg_user.username,
            user.telegram_id,
            tg_user.language_code,
            can_open_chat=not chat_info.has_private_forwards,
        ),
        reply_markup=_ban_keyboard(user.telegram_id),
    )
    return ticket


@router.message()
async def relay_to_support(message: Message, bot: Bot, session: AsyncSession) -> None:
    tg_user = message.from_user
    user, is_new_user = await get_or_create_user(
        session,
        telegram_id=tg_user.id,
        full_name=tg_user.full_name,
        username=tg_user.username,
    )
    locale = resolve_locale(user.locale or tg_user.language_code)

    if user.is_banned:
        await message.answer(t(locale, "banned"))
        return

    if is_new_user:
        await message.answer(t(locale, "welcome", org=html.escape(settings.support_org_name)))

    ticket = await get_open_ticket(session, user)

    reply_parameters = None
    if ticket is not None and message.reply_to_message is not None:
        group_message_id = await find_group_message_id(
            session, ticket.id, message.reply_to_message.message_id
        )
        if group_message_id is not None:
            reply_parameters = ReplyParameters(
                message_id=group_message_id, allow_sending_without_reply=True
            )

    if ticket is not None:
        try:
            copy = await message.copy_to(
                chat_id=settings.support_chat_id,
                message_thread_id=ticket.thread_id,
                reply_parameters=reply_parameters,
            )
        except TelegramBadRequest as error:
            if "thread not found" not in error.message.lower():
                raise
            await close_ticket(session, ticket)
            ticket = None
        else:
            await record_relayed_message(session, ticket.id, message.message_id, copy.message_id)
            await session.commit()
            return

    ticket = await _open_ticket(bot, session, user, tg_user)
    copy = await message.copy_to(
        chat_id=settings.support_chat_id,
        message_thread_id=ticket.thread_id,
    )
    await record_relayed_message(session, ticket.id, message.message_id, copy.message_id)
    await session.commit()
