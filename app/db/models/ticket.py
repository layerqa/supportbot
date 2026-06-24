from __future__ import annotations

import enum
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.mixins import TimestampMixin

if TYPE_CHECKING:
    from app.db.models.user import User


class TicketStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"


class Ticket(Base, TimestampMixin):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    thread_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    status: Mapped[TicketStatus] = mapped_column(default=TicketStatus.OPEN)

    user: Mapped["User"] = relationship(back_populates="tickets")
