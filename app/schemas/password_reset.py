from pydantic import BaseModel, EmailStr, field_validator, FieldValidationInfo

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordResponse(BaseModel):
    message: str  # 운영에서는 토큰/개발정보 없음
    reset_token_for_dev: str | None = None  #  운영에선 항상 null

class ResetPasswordRequest(BaseModel):
    token: str
    new_password1: str
    new_password2: str

    @field_validator("new_password1", "new_password2", mode="after")
    @classmethod
    def not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v

    @field_validator("new_password2", mode="after")
    @classmethod
    def pw_match(cls, v: str, info: FieldValidationInfo) -> str:
        if v != info.data.get("new_password1"):
            raise ValueError("비밀번호가 일치하지 않습니다.")
        return v

class ResetPasswordResponse(BaseModel):
    message: str

