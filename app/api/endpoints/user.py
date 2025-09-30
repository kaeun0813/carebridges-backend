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
    # 이메일 중복 검사 (비즈니스 로직)
    if get_user_by_email(db, user_create.email):
        # 중복은 409 추천 (콘플릭트)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "message": "이미 등록된 이메일입니다.",
                "errors": [
                    {"field": "email", "message": "이미 등록된 이메일입니다.", "code": "duplicate"}
                ],
            },
        )

    # 여기까지 오면 Pydantic이 name/비밀번호/전화번호 검증을 이미 끝낸 상태
    return create_simple_user(db, user_create)


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "email": current_user.email,
        "name": current_user.name,
        "phone": current_user.phone,
    }