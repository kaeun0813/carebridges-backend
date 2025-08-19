from sqlalchemy import Column, Integer, Text, String, ForeignKey, DateTime, func
from app.db.base import Base

class FAQCategory(Base):
    __tablename__ = "faq_categories"

    category_id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)

class FAQQuestion(Base):
    __tablename__ = "faq_questions"

    question_id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("faq_categories.category_id"), nullable=False)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    reference_title = Column(String(255))
    reference_url = Column(Text)
    created_at = Column(DateTime, server_default=func.now())  # 자동 타임스탬프