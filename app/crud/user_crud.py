from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.utils.security import get_password_hash


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_create: UserCreate) -> User:
    # 비밀번호 해싱
    hashed_pw = get_password_hash(user_create.password1)

    # 사용자 인스턴스 생성
    user = User(
        name=user_create.name,
        phone=user_create.phone,
        email=user_create.email,
        password=hashed_pw, 
        organization=user_create.organization,
        position=user_create.position,
        region=user_create.region
    )

    # DB 저장
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
