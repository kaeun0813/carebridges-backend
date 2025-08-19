from sqlalchemy import (
    Column, BigInteger, Integer, String, Text, Enum, ForeignKey, DateTime, Double
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

class Conversation(Base):
    __tablename__ = "conversations"

    conversation_id = Column(BigInteger, primary_key=True, autoincrement=True)
    worker_id = Column(
        Integer,
        ForeignKey("social_workers.worker_id", ondelete="CASCADE"),  
        nullable=False,
        index=True,
    )
    title = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan"
    )
    worker = relationship("User", back_populates="conversations")

class Message(Base):
    __tablename__ = "messages"

    message_id = Column(BigInteger, primary_key=True, autoincrement=True)
    conversation_id = Column(
        BigInteger,
        ForeignKey("conversations.conversation_id", ondelete="CASCADE"), 
        nullable=False,
        index=True,
    )
    worker_id = Column(
        Integer,
        ForeignKey("social_workers.worker_id", ondelete="CASCADE"),       
        nullable=False,
        index=True,
    )
    sender = Column(Enum("user", "assistant", name="sender_enum"), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(Enum("saved", "completed", "failed", name="status_enum"), default="saved")
    token_usage = Column(Integer, default=0)
    latency_ms = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    conversation = relationship("Conversation", back_populates="messages")
    sources = relationship("MessageSource", back_populates="message", cascade="all, delete-orphan")

class MessageSource(Base):
    __tablename__ = "message_sources"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message_id = Column(BigInteger, ForeignKey("messages.message_id", ondelete="CASCADE"), nullable=False, index=True)  # ✅ 권장
    source_title = Column(String(512))
    source_url = Column(String(1024))
    snippet = Column(Text)
    score = Column(Double)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    message = relationship("Message", back_populates="sources")
