from sqlalchemy import Column, Integer, String, DateTime, Enum, Date, func
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
    job_title = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    experience = Column(Integer, nullable=False)
    region = Column(String(100))
    ai_data_consent = Column(Enum('Yes', 'No'), default='No')
    marketing_consent_status = Column(Enum('Yes', 'No'), default='No')
    marketing_consent_channel = Column(String(20))  # SET 타입은 문자열로 처리 (ex. 'SMS,Email')
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    

    # 기존 User 클래스 내부에 추가
    chats = relationship("ChatLog", back_populates="worker", cascade="all, delete", passive_deletes=True)
