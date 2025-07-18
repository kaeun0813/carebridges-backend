from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserOut
from app.crud.user_crud import get_user_by_email, create_user
from app.db.session import get_db

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=201)
def register_user(user_create: UserCreate, db: Session = Depends(get_db)):
    # 중복 이메일 검사
    existing_user = get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )

    # 비밀번호 일치 여부는 이미 Pydantic에서 검증했다고 가정
    user = create_user(db, user_create)
    return user
