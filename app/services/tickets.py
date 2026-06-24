from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.models.ticket import Ticket, TicketStatus
from app.db.models.user import User


async def get_open_ticket(session: AsyncSession, user: User) -> Ticket | None:
    return await session.scalar(
        select(Ticket).where(
            Ticket.user_id == user.id, Ticket.status == TicketStatus.OPEN
        )
    )


async def get_ticket_by_thread(session: AsyncSession, thread_id: int) -> Ticket | None:
    return await session.scalar(
        select(Ticket)
        .where(Ticket.thread_id == thread_id)
        .options(selectinload(Ticket.user))
    )


async def create_ticket(session: AsyncSession, user: User, thread_id: int) -> Ticket:
    ticket = Ticket(user=user, thread_id=thread_id)
    session.add(ticket)
    await session.flush()
    return ticket


async def close_ticket(session: AsyncSession, ticket: Ticket) -> None:
    ticket.status = TicketStatus.CLOSED
    await session.flush()
