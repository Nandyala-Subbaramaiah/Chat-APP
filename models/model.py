from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base  # make sure this points to your Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    # define relationship to chats
    chats = relationship("Chat", back_populates="creator")
    chat_memberships = relationship("ChatMember", back_populates="user")


class Chat(Base):
    __tablename__ = "chats"  # changed to plural to match foreign keys

    id = Column(Integer, primary_key=True)
    message = Column(String, nullable=False)
    created_by = Column(String, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime)

    creator = relationship("User", back_populates="chats")
    members = relationship("ChatMember", back_populates="chat")


class ChatMember(Base):
    __tablename__ = "chat_members"

    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer, ForeignKey("chats.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    role = Column(String, default="member")  # member / admin

    chat = relationship("Chat", back_populates="members")
    user = relationship("User", back_populates="chat_memberships")
