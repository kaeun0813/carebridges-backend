import re
from pydantic import BaseModel, EmailStr, field_validator, FieldValidationInfo
from typing import Optional
from datetime import datetime

# 전화번호 정규식 (하이픈 필수)
PHONE_RE = re.compile(r"^01[016789]-\d{3,4}-\d{4}$")

class SimpleUserCreate(BaseModel):
    email: EmailStr
    name: str
    password1: str
    password2: str
    phone: str

    # 공통 빈값 방지
    @field_validator("email", "name", "password1", "password2", "phone", mode="after")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

    # 비밀번호 일치 검증
    @field_validator("password2", mode="after")
    @classmethod
    def passwords_match(cls, v: str, info: FieldValidationInfo) -> str:
        pw1 = info.data.get("password1")
        if pw1 is not None and v != pw1:
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v

    # 전화번호 형식 검증 
    @field_validator("phone", mode="after")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not PHONE_RE.fullmatch(v):
            raise ValueError("전화번호 형식이 올바르지 않습니다. 예: 010-1234-5678")
        return v


class UserOut(BaseModel):
    worker_id: int
    email: str
    name: str
    phone: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
