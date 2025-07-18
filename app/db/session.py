from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.db.base import Base 

# DB 연결 엔진 생성
#engine = create_engine(settings.DATABASE_URL)
DATABASE_URL = settings.DATABASE_URL
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)
# 세션 로컬 클래스 (의존성 주입용)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# DB 세션 가져오기 (FastAPI Depends용)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()