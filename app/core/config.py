from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, Field
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str  
    ACCESS_TOKEN_EXPIRE_MINUTES: int  
    AI_SERVER_URL: AnyHttpUrl = Field(default="http://127.0.0.1:8001/chat")
    REFRESH_TOKEN_EXPIRE_DAYS: int 

    FRONTEND_BASE_URL: str = "https://your-frontend.example.com"  # 리셋 링크 생성용

    # 메일 설정 
    SMTP_HOST: str = "smtp.example.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = "user"
    SMTP_PASSWORD: str = "pass"
    SMTP_USE_TLS: bool = True
    MAIL_FROM: str = "no-reply@example.com"
    MAIL_SUBJECT_RESET: str = "[Carebridges] 비밀번호 재설정 안내"
    
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
