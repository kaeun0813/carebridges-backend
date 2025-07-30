from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.user import SimpleUserCreate, UserOut
from app.crud.user_crud import get_user_by_email, create_simple_user
from app.db.session import get_db

router = APIRouter()

@router.post("/register", response_model=UserOut, status_code=201)
def register_user(user_create: SimpleUserCreate, db: Session = Depends(get_db)):
    existing_user = get_user_by_email(db, user_create.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다."
        )
    return create_simple_user(db, user_create)
