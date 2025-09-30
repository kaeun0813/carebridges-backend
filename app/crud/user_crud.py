from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import SimpleUserCreate
from app.utils.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

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
