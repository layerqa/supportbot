from aiogram import Bot, Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.chat_type import ChatTypeFilter
from app.config import settings
from app.services.tickets import create_ticket, get_open_ticket
from app.services.users import get_or_create_user

router = Router(name="support")
router.message.filter(ChatTypeFilter("private"))


@router.message()
async def relay_to_support(message: Message, bot: Bot, session: AsyncSession) -> None:
    tg_user = message.from_user
    user = await get_or_create_user(
        session,
        telegram_id=tg_user.id,
        full_name=tg_user.full_name,
        username=tg_user.username,
    )

    ticket = await get_open_ticket(session, user)
    if ticket is None:
        topic = await bot.create_forum_topic(
            chat_id=settings.support_chat_id,
            name=f"{user.full_name} (id{user.telegram_id})",
        )
        ticket = await create_ticket(session, user, thread_id=topic.message_thread_id)

    await message.copy_to(
        chat_id=settings.support_chat_id,
        message_thread_id=ticket.thread_id,
    )
    await session.commit()
