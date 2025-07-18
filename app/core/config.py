from pydantic_settings import BaseSettings

class Settings(BaseSettings): 
    DATABASE_URL: str = "sqlite:///./test.db"  # 기본값으로 SQLite 경로 
    SECRET_KEY: str = "your-secret-key"
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
