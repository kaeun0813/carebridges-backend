from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.crud.user_crud import get_user_by_email
from app.utils.security import verify_password
from app.utils.jwt import create_access_token
from app.schemas.token import Token
from app.models.user import User
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user: User = get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="이메일이 올바르지 않습니다.")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="비밀번호가 올바르지 않습니다.")


    access_token = create_access_token(
        data={"sub": str(user.worker_id)},  # 토큰에 worker_id 넣기
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}

