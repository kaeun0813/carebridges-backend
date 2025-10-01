from sqlalchemy.orm import Session
from datetime import datetime, timedelta         
import hashlib, secrets  

from app.models.user import User
from app.models.password_reset_token import PasswordResetToken
from app.schemas.user import SimpleUserCreate
from app.utils.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()

def get_user_by_name_phone(db: Session, name: str, phone: str):
    return db.query(User).filter(User.name == name, User.phone == phone).first()


def create_simple_user(db: Session, user_create: SimpleUserCreate) -> User:
    hashed_pw = get_password_hash(user_create.password1)
    user = User(
        email=user_create.email,
        name=user_create.name,
        password=hashed_pw,
        phone=user_create.phone,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
# ===== 비밀번호 재설정 관련 =====

# 토큰 생성 (원문 토큰은 이메일로만 전달, DB에는 해시만 저장) 
def create_password_reset_token(db: Session, user_id: int, ttl_minutes: int = 30) -> str:
    raw_token = secrets.token_urlsafe(32)
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    expires_at = datetime.utcnow() + timedelta(minutes=ttl_minutes)

    prt = PasswordResetToken(
        user_id=user_id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.add(prt)
    db.commit()
    return raw_token  # 이메일 링크에 이 원문 토큰을 사용


# 토큰 검증 + 1회성 소모  # [ADDED]
def verify_and_consume_reset_token(db: Session, raw_token: str) -> User | None:
    token_hash = hashlib.sha256(raw_token.encode("utf-8")).hexdigest()
    prt = (
        db.query(PasswordResetToken)
        .filter(
            PasswordResetToken.token_hash == token_hash,
            PasswordResetToken.used == False,
        )
        .first()
    )
    if not prt:
        return None
    if prt.expires_at < datetime.utcnow():
        return None

    prt.used = True
    db.add(prt)
    db.commit()

    return db.query(User).filter(User.worker_id == prt.user_id).first()


# 비밀번호 변경  # [ADDED]
def update_user_password(db: Session, user: User, new_password: str) -> None:
    user.password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    # 필요하면 db.refresh(user) 추가 가능