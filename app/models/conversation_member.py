# models/conversation_member.py

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class ConversationMember(Base):
    __tablename__ = "conversation_members"

    __table_args__ = (
        UniqueConstraint(
            "conversation_id",
            "user_id",
            name="unique_conversation_user"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE")
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE")
    )

    conversation = relationship(
        "Conversation",
        back_populates="members"
    )

    user = relationship(
        "User",
        back_populates="conversation_members"
    )