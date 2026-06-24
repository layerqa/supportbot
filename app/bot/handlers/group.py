from aiogram import Router
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.chat_type import ChatTypeFilter
from app.config import settings
from app.services.tickets import get_ticket_by_thread

router = Router(name="group")
router.message.filter(ChatTypeFilter(("group", "supergroup")))


@router.message()
async def relay_to_user(message: Message, session: AsyncSession) -> None:
    if message.chat.id != settings.support_chat_id or message.message_thread_id is None:
        return

    ticket = await get_ticket_by_thread(session, message.message_thread_id)
    if ticket is None:
        return

    await message.copy_to(chat_id=ticket.user.telegram_id)
