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
        job_title=user_create.job_title,
        start_date=user_create.start_date,
        experience=user_create.experience,
        region=user_create.region,
        ai_data_consent=user_create.ai_data_consent,
        marketing_consent_status=user_create.marketing_consent_status,
        marketing_consent_channel=user_create.marketing_consent_channel
    )


    # DB 저장
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
