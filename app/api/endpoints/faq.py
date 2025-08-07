from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.faq import FAQCategorySchema, FAQQuestionListSchema, FAQQuestionDetailSchema
from app.crud import faq_crud

router = APIRouter()

# (1) 카테고리 목록 조회 - 비로그인 허용
@router.get("/categories", response_model=List[FAQCategorySchema])
def get_categories(db: Session = Depends(get_db)):
    return faq_crud.get_all_categories(db)


# (2) 질문 목록 조회 - 비로그인 허용 (답변 없이)
@router.get("/questions", response_model=List[FAQQuestionListSchema])
def get_questions(
    category_id: Optional[int] = Query(None, description="카테고리 ID"),
    db: Session = Depends(get_db)
):
    return faq_crud.get_questions(db, category_id)


# (3) 질문 상세 조회 - 로그인한 사용자만 answer 포함
@router.get("/questions/{question_id}", response_model=FAQQuestionDetailSchema)
def get_question_detail(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    question = faq_crud.get_question_by_id(db, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="질문을 찾을 수 없습니다.")
    return question
