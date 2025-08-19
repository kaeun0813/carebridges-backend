from datetime import datetime, timedelta
from jose import JWTError, jwt, ExpiredSignatureError
from fastapi import HTTPException, status
from app.core.config import settings

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    액세스 토큰 생성 (기본 15분 유효)
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    리프레시 토큰 생성 (기본 7일 유효)
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str, secret_key: str) -> dict:
    """
    토큰 유효성 검증 함수 - Access / Refresh 구분 없이 사용 가능
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=[settings.ALGORITHM])
        return payload

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="토큰이 만료되었습니다. 다시 로그인해주세요.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Access Token 전용 검증 함수
def verify_access_token(token: str) -> dict:
    return verify_token(token, settings.SECRET_KEY)


# Refresh Token 전용 검증 함수
def verify_refresh_token(token: str) -> dict:
    return verify_token(token, settings.REFRESH_SECRET_KEY)
