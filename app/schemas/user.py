from pydantic import BaseModel, EmailStr, field_validator, FieldValidationInfo
from typing import Optional, Literal
from datetime import datetime, date

class UserCreate(BaseModel):
    email: EmailStr
    phone: str
    password1: str
    password2: str
    name: str
    organization: str
    job_title: str
    start_date: date
    experience: int
    region: Optional[str] = None
    ai_data_consent: Optional[str] = "No"
    marketing_consent_status: Optional[str] = "No"
    marketing_consent_channel: Optional[str] = None

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


class UserOut(BaseModel):
    worker_id: int
    name: str
    phone: str
    email: str
    organization: str
    job_title: str
    start_date: date
    experience: int
    region: Optional[str] = None
    ai_data_consent: Optional[str] = "No"
    marketing_consent_status: Optional[str] = "No"
    marketing_consent_channel: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
