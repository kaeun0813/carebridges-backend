from fastapi import APIRouter, Depends, HTTPException, status, Body ,Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.session import get_db
from app.crud.user_crud import get_user_by_email
from app.utils.security import verify_password
from app.utils.jwt import create_access_token, create_refresh_token, verify_refresh_token
from app.schemas.token import Token
from app.models.user import User
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

# 로그인: 액세스 토큰은 응답 본문, 리프레시 토큰은 HttpOnly 쿠키
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user: User = get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="이메일이 올바르지 않습니다.")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="비밀번호가 올바르지 않습니다.")

    access_token = create_access_token(
        data={"sub": str(user.worker_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.worker_id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    # refresh_token은 쿠키에 저장
    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer"
    })
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure= True,  # HTTPS 환경에서만 전송 (운영 시 True 권장)
        samesite="strict",  # CSRF 방지
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
        path="/auth/refresh"
    )
    return response


@router.post("/refresh", response_model=Token)
def refresh_token_endpoint(
    request: Request,
    db: Session = Depends(get_db)
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh Token이 없습니다.")

    payload = verify_refresh_token(refresh_token)
    user_id = payload.get("sub")

    user = db.query(User).filter(User.worker_id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    access_token = create_access_token(
        data={"sub": str(user.worker_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    #  새 리프레시 토큰도 쿠키로 갱신
    new_refresh_token = create_refresh_token(
        data={"sub": str(user.worker_id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )

    response = JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer"
    })
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
        path="/auth/refresh"
    )
    return response

@router.post("/logout")
def logout(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=400,
            detail="로그인 상태가 아닙니다. (Refresh Token 없음)"
        )

    response = JSONResponse(content={"message": "로그아웃 되었습니다."})
    response.delete_cookie(
        key="refresh_token",
        path="/auth/refresh"
    )
    return response