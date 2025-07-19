from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.utils.jwt import verify_access_token
from fastapi.security import OAuth2PasswordBearer

#OAuth2 비밀번호 기반 토큰 스키마 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# 현재 로그인된 사용자 가져오기
def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)  # 토큰 스키마가 설정돼 있어야 함
) -> User:
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰 인증 실패",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰에 사용자 정보 없음",
        )

    user = db.query(User).filter(User.worker_id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다.",
        )
    return user
