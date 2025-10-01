from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class PasswordResetToken(Base):
    __tablename__ = "password_reset_tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("social_workers.worker_id", ondelete="CASCADE"), nullable=False)
    token_hash = Column(String(128), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, nullable=False, server_default="0")
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", backref="password_reset_tokens")
