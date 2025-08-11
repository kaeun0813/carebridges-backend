from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import SimpleUserCreate, UserOut
from app.crud.user_crud import get_user_by_email, create_simple_user
from app.db.session import get_db
from app.models.user import User
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
def register_user(user_create: SimpleUserCreate, db: Session = Depends(get_db)):

    #  이메일 중복 검사
    existing_user = get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    #  필수 필드 누락 검사
    if not user_create.email or not user_create.name or not user_create.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="필수 입력 항목(이메일, 이름, 비밀번호)을 모두 입력해주세요."
        )

    #  이메일 형식 검증 (간단한 예시)
    if "@" not in user_create.email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="올바른 이메일 형식이 아닙니다."
        )
    
    return create_simple_user(db, user_create)


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "name": current_user.name,
    }