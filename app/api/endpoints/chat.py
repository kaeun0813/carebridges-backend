from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ChatCreate, ChatOut, ChatInput, ChatResponse
from app.crud import chat_crud  # CRUD 모듈 사용
from fastapi import Query


router = APIRouter()

# POST /chat/logs - 대화 저장
@router.post("/logs", response_model=ChatOut, status_code=201)
def create_chat_log(
    chat_create: ChatCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return chat_crud.create_chat_log(db, chat_create, current_user.worker_id)


# GET /chat/logs - 전체 대화 조회
@router.get("/logs", response_model=List[ChatOut])
def get_chat_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return chat_crud.get_chat_logs_by_user(db, current_user.worker_id)

# POST /chat/ask - 사용자 질문 → 챗봇 응답 → 저장
@router.post("/ask", response_model=ChatResponse)
def ask_chatbot(
    chat_input: ChatInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user_msg = chat_input.user_message
    dummy_bot_response = "테스트 응답입니다."  # GPT 연동 예정

    chat_crud.save_chat(db, current_user.worker_id, user_msg, "user")
    chat_crud.save_chat(db, current_user.worker_id, dummy_bot_response, "bot")

    return ChatResponse(bot_message=dummy_bot_response)

#GET /chat/logs/recent - 최근 대화 n개 조회
@router.get("/logs/recent", response_model=List[ChatOut])
def get_recent_chats(
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return chat_crud.get_recent_chat_logs(db, current_user.worker_id, limit)
