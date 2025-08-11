from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.faq import FAQCategory
from app.schemas.faq import FAQCategorySchema, FAQQuestionListSchema, FAQQuestionDetailSchema
from app.crud import faq_crud

router = APIRouter()

# (1) 카테고리 목록 조회 - 비로그인 허용
@router.get("/categories", response_model=List[FAQCategorySchema])
def get_categories(db: Session = Depends(get_db)):
    try:
        categories = faq_crud.get_all_categories(db)
        # 빈 배열은 정상 응답
        return categories
    except SQLAlchemyError:
        # DB 에러는 500
        raise HTTPException(status_code=500, detail="카테고리 조회 중 서버 오류가 발생했습니다.")
        

# (2) 질문 목록 조회 - 비로그인 허용 (답변 없이)
@router.get("/questions", response_model=List[FAQQuestionListSchema])
def get_questions(
    category_id: Optional[int] = Query(None, description="카테고리 ID"),
    db: Session = Depends(get_db)
):
    try:
        # 선택적: category_id 값 범위 검증
        if category_id is not None and category_id <= 0:
            raise HTTPException(status_code=400, detail="유효하지 않은 카테고리 ID입니다. (양의 정수)")

        # category_id가 주어졌다면 실제 존재하는 카테고리인지 확인
        if category_id is not None:
            exists = (
                db.query(FAQCategory)
                  .filter(FAQCategory.category_id == category_id)
                  .first()
            )
            if not exists:
                raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

        questions = faq_crud.get_questions(db, category_id)
        # 빈 배열은 정상 응답
        return questions

    except HTTPException:
        # 위에서 명시적으로 올린 예외는 그대로 전달
        raise
    except SQLAlchemyError:
        # DB 에러는 500
        raise HTTPException(status_code=500, detail="질문 목록 조회 중 서버 오류가 발생했습니다.")



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
