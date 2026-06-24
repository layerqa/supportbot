from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, ReplyParameters
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.filters.chat_type import ChatTypeFilter
from app.config import settings
from app.services.messages import find_user_message_id, record_relayed_message
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

    reply_parameters = None
    if message.reply_to_message is not None:
        user_message_id = await find_user_message_id(
            session, ticket.id, message.reply_to_message.message_id
        )
        if user_message_id is not None:
            reply_parameters = ReplyParameters(
                message_id=user_message_id, allow_sending_without_reply=True
            )

    copy = await message.copy_to(
        chat_id=ticket.user.telegram_id,
        reply_parameters=reply_parameters,
    )
    await record_relayed_message(session, ticket.id, copy.message_id, message.message_id)
    await session.commit()


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
