from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, Field
class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    REFRESH_SECRET_KEY: str
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 
    REFRESH_TOKEN_EXPIRE_DAYS: int 
    AI_SERVER_URL: AnyHttpUrl = Field(default="http://127.0.0.1:8001/chat")

    class Config:
        env_file = ".env"

settings = Settings()