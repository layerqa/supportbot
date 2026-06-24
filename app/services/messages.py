from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.relayed_message import RelayedMessage


async def record_relayed_message(
    session: AsyncSession, ticket_id: int, user_message_id: int, group_message_id: int
) -> None:
    session.add(
        RelayedMessage(
            ticket_id=ticket_id,
            user_message_id=user_message_id,
            group_message_id=group_message_id,
        )
    )
    await session.flush()


async def find_group_message_id(
    session: AsyncSession, ticket_id: int, user_message_id: int
) -> int | None:
    return await session.scalar(
        select(RelayedMessage.group_message_id).where(
            RelayedMessage.ticket_id == ticket_id,
            RelayedMessage.user_message_id == user_message_id,
        )
    )


async def find_user_message_id(
    session: AsyncSession, ticket_id: int, group_message_id: int
) -> int | None:
    return await session.scalar(
        select(RelayedMessage.user_message_id).where(
            RelayedMessage.ticket_id == ticket_id,
            RelayedMessage.group_message_id == group_message_id,
        )
    )
