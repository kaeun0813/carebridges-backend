# app/schemas/auth.py
import re
from pydantic import BaseModel, EmailStr, field_validator

# 프론트 정책: 하이픈 필수 "010-1234-5678"
PHONE_RE = re.compile(r"^01[016789]-\d{3,4}-\d{4}$")

class FindEmailRequest(BaseModel):
    name: str
    phone: str

    @field_validator("name", "phone", mode="after")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

    @field_validator("phone", mode="after")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if not PHONE_RE.fullmatch(v):
            raise ValueError("전화번호 형식이 올바르지 않습니다. 예: 010-1234-5678")
        return v

class FindEmailResponse(BaseModel):
    email: EmailStr  # 전체 이메일 반환
