from pydantic import BaseModel, EmailStr, field_validator, FieldValidationInfo
from typing import Optional
from datetime import datetime

class SimpleUserCreate(BaseModel):
    email: EmailStr
    name: str
    password1: str
    password2: str

    @field_validator("email", "name", "password1", "password2")
    def not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

    @field_validator("password2")
    def passwords_match(cls, v: str, info: FieldValidationInfo) -> str:
        if v != info.data.get("password1"):
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
