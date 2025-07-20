from sqlalchemy import Column, Integer, Text, Enum, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
from sqlalchemy.orm import relationship

class ChatLog(Base):
    __tablename__ = "chat_logs"

    chat_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    worker_id = Column(Integer, ForeignKey("social_workers.worker_id", ondelete="CASCADE"), nullable=False)
    message = Column(Text, nullable=False)
    sender = Column(Enum("bot", "user", name="sender_enum"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


    # 관계 설정
    worker = relationship("User", back_populates="chats")