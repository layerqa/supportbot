from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.chat_type import ChatTypeFilter
from app.config import settings
from app.services.tickets import get_ticket_by_thread
from app.services.users import ban_user

router = Router(name="group")
router.message.filter(ChatTypeFilter(("group", "supergroup")))
router.callback_query.filter(ChatTypeFilter(("group", "supergroup")))


@router.message()
async def relay_to_user(message: Message, session: AsyncSession) -> None:
    if message.chat.id != settings.support_chat_id or message.message_thread_id is None:
        return

    ticket = await get_ticket_by_thread(session, message.message_thread_id)
    if ticket is None:
        return

    await message.copy_to(chat_id=ticket.user.telegram_id)


@router.callback_query(F.data.startswith("ban:"))
async def on_ban_user(callback: CallbackQuery, session: AsyncSession) -> None:
    if callback.message.chat.id != settings.support_chat_id:
        await callback.answer()
        return

    if callback.from_user.id not in settings.admin_ids:
        await callback.answer("Недостаточно прав для этого действия", show_alert=True)
        return

    telegram_id = int(callback.data.split(":", 1)[1])
    user = await ban_user(session, telegram_id)
    await session.commit()

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.answer(
        f"🚫 Пользователь {user.full_name} заблокирован и больше не сможет писать в поддержку."
    )
    await callback.answer("Пользователь заблокирован")
