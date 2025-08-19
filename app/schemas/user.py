from pydantic import BaseModel, EmailStr, field_validator, FieldValidationInfo
from typing import Optional
from datetime import datetime

class SimpleUserCreate(BaseModel):
    email: EmailStr
    name: str
    password1: str
    password2: str

    # 공통 빈값 방지
    @field_validator("email", "name", "password1", "password2", mode="after")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

    # 비밀번호 일치 검증: password2에 에러 매핑
    @field_validator("password2", mode="after")
    @classmethod
    def passwords_match(cls, v: str, info: FieldValidationInfo) -> str:
        pw1 = info.data.get("password1")
        if pw1 is not None and v != pw1:
            # 이 예외는 password2 필드의 검증 에러로 연결됩니다 (422)
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v

class UserOut(BaseModel):
    worker_id: int
    email: str
    name: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
