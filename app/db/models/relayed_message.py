from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class RelayedMessage(Base):
    __tablename__ = "relayed_messages"

    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(
        ForeignKey("tickets.id", ondelete="CASCADE"), index=True
    )
    user_message_id: Mapped[int] = mapped_column(BigInteger, index=True)
    group_message_id: Mapped[int] = mapped_column(BigInteger, index=True)
