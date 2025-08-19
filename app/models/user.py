from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.base import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "social_workers"  #mysql 실제 테이블명

    worker_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True)
    password = Column(String(255), nullable=False)
    organization = Column(String(100))
    position = Column(String(50))
    region = Column(String(100))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    conversations = relationship(
        "Conversation",                   # 연결할 대상 클래스 이름 (문자열로)
        back_populates="worker",          # Conversation 쪽의 관계 이름과 매칭
        cascade="all, delete",            # 사용자 삭제 시 대화도 함께 삭제
        passive_deletes=True              # DB 수준의 ON DELETE 적용
    )
