from pydantic import BaseModel, EmailStr, field_validator, FieldValidationInfo
from typing import Optional
from datetime import datetime

# 요청 시: 회원가입 입력값
class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    password1: str
    password2: str
    name: str
    organization: Optional[str] = None
    position: Optional[str] = None
    region: Optional[str] = None

    @field_validator('name', 'password1', 'password2', 'email')
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('password2')
    def passwords_match(cls, v: str, info: FieldValidationInfo) -> str:
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError('비밀번호가 일치하지 않습니다.')
        return v


# 응답 시: 유저 정보 반환
class UserOut(BaseModel):
    worker_id: int
    name: str
    phone: str
    email: Optional[str] = None
    organization: Optional[str] = None
    position: Optional[str] = None
    region: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # SQLAlchemy 모델 ↔ Pydantic 호환 설정
