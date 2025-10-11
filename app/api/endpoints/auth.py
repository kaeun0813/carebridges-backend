from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
import logging

from app.db.session import get_db
from app.crud.user_crud import (
    get_user_by_email,
    get_user_by_name_phone,
    create_password_reset_token,
    verify_and_consume_reset_token,
    update_user_password,
    get_user_by_name_email,
)
from app.utils.security import verify_password
from app.utils.jwt import create_access_token, create_refresh_token, verify_refresh_token
from app.schemas.token import Token
from app.schemas.auth import FindEmailRequest, FindEmailResponse
from app.schemas.password_reset import (
    ForgotPasswordRequest,
    ForgotPasswordResponse,
    ResetPasswordRequest,
    ResetPasswordResponse,
)
from app.core.config import settings
from app.models.user import User
from app.utils.mailer import send_email_html

logger = logging.getLogger(__name__)

router = APIRouter()

# ----------------------------------------
# 로그인: 액세스 토큰은 응답 본문, 리프레시 토큰은 HttpOnly 쿠키
# ----------------------------------------
@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user: User = get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이메일이 올바르지 않습니다.")

    if not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="비밀번호가 올바르지 않습니다.")

    access_token = create_access_token(
        data={"sub": str(user.worker_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.worker_id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    # refresh_token은 쿠키에 저장
    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=True,                # 운영 환경에서 HTTPS 권장
        samesite="strict",          # CSRF 방지
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
        path="/auth/refresh",
    )
    return response


# ----------------------------------------
# 액세스 토큰 재발급(리프레시 토큰 검증)
# ----------------------------------------
@router.post("/refresh", response_model=Token)
def refresh_token_endpoint(
    request: Request,
    db: Session = Depends(get_db),
):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh Token이 없습니다.")

    payload = verify_refresh_token(refresh_token)
    user_id = payload.get("sub")

    user = db.query(User).filter(User.worker_id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다.")

    access_token = create_access_token(
        data={"sub": str(user.worker_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    # 새 리프레시 토큰도 쿠키로 갱신
    new_refresh_token = create_refresh_token(
        data={"sub": str(user.worker_id)},
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )

    response = JSONResponse(
        content={
            "access_token": access_token,
            "token_type": "bearer",
        }
    )
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=60 * 60 * 24 * settings.REFRESH_TOKEN_EXPIRE_DAYS,
        path="/auth/refresh",
    )
    return response


# ----------------------------------------
# 로그아웃: 리프레시 토큰 쿠키 삭제
# ----------------------------------------
@router.post("/logout")
def logout(request: Request):
    refresh_token = request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="로그인 상태가 아닙니다. (Refresh Token 없음)",
        )

    response = JSONResponse(content={"message": "로그아웃 되었습니다."})
    response.delete_cookie(
        key="refresh_token",
        path="/auth/refresh",
    )
    return response


# ----------------------------------------
# 아이디(이메일) 찾기: 이름 + 전화번호로 조회(전체 이메일 반환)
# ----------------------------------------
@router.post("/find-email", response_model=FindEmailResponse, status_code=status.HTTP_200_OK)
def find_email(payload: FindEmailRequest, db: Session = Depends(get_db)):
    user = get_user_by_name_phone(db, payload.name, payload.phone)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"message": "일치하는 회원을 찾을 수 없습니다."},
        )
    return FindEmailResponse(email=user.email)


# ----------------------------------------
# 비밀번호 재설정 1단계: 이름 + 이메일 확인 후 메일 발송
# ----------------------------------------
@router.post("/forgot-password", response_model=ForgotPasswordResponse, status_code=status.HTTP_200_OK)
def forgot_password(payload: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = get_user_by_name_email(db, payload.name.strip(), payload.email)

    token_for_dev = None
    if user:
        raw_token = create_password_reset_token(db, user.worker_id, ttl_minutes=30)
        reset_link = f"{settings.FRONTEND_BASE_URL}/reset-password?token={raw_token}"

        body = f"""
        <p>안녕하세요, 비밀번호 재설정 안내입니다.</p>
        <p>아래 링크를 클릭하여 새 비밀번호를 설정해 주세요.</p>
        <p><a href="{reset_link}">{reset_link}</a></p>
        <p>해당 링크는 30분 후 만료됩니다.</p>
        """

        try:
            send_email_html(to_email=user.email, subject=settings.MAIL_SUBJECT_RESET, body_html=body)
            logger.info("비밀번호 재설정 메일 발송 성공: %s", user.email,user.name)
        except Exception as e:
            logger.exception("비밀번호 재설정 메일 발송 실패: %s", e)

        if settings.DEBUG:
            token_for_dev = raw_token
            logger.info("[DEV] reset token for %s: %s", user.email, user.name, raw_token)

    return ForgotPasswordResponse(
        message="비밀번호 재설정 안내를(계정이 존재한다면) 전송했습니다.",
        reset_token_for_dev=token_for_dev,
    )


# 비밀번호 재설정 2단계
@router.post("/reset-password", response_model=ResetPasswordResponse, status_code=status.HTTP_200_OK)
def reset_password(payload: ResetPasswordRequest, db: Session = Depends(get_db)):
    user = verify_and_consume_reset_token(db, payload.token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "유효하지 않거나 만료된 토큰입니다.", "code": "TOKEN_INVALID"},
        )

    update_user_password(db, user, payload.new_password1)
    logger.info("비밀번호 재설정 완료: user_id=%s", user.worker_id)

    return ResetPasswordResponse(message="비밀번호가 변경되었습니다.")