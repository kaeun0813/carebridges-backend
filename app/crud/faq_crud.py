from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.faq import FAQCategory, FAQQuestion

def get_all_categories(db: Session) -> List[FAQCategory]:
    return db.query(FAQCategory).all()

def get_questions(db: Session, category_id: Optional[int] = None) -> List[FAQQuestion]:
    query = db.query(FAQQuestion)
    if category_id:
        query = query.filter(FAQQuestion.category_id == category_id)
    return query.all()

def get_question_by_id(db: Session, question_id: int) -> Optional[FAQQuestion]:
    return db.query(FAQQuestion).filter(FAQQuestion.question_id == question_id).first()
