from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.chat import (
    ConversationCreate,
    MessageCreate,
    MessageOut,
    ConversationOut,
    ConversationWithMessages,
    MessageWithAIRequest,
    MessageWithAIResponse,
)
from app.crud import chat_crud
from app.api.deps import get_current_user
from app.models.user import User
from app.services.chat_ai import call_ai_server

router = APIRouter()

# 1) 대화 생성
@router.post("/conversations", response_model=ConversationOut)
def create_conversation(
    payload: ConversationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = chat_crud.create_conversation(
        db=db,
        worker_id=current_user.worker_id,   # ✅ id → worker_id
        conversation_in=payload,
    )
    return conversation

# 2) 메시지 추가
@router.post("/messages", response_model=MessageOut)
def add_message(
    payload: MessageCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # 소유한 conversation인지 확인
    is_owner = chat_crud.get_conversation_owner_check(
        db=db,
        conversation_id=payload.conversation_id,
        worker_id=current_user.worker_id,     # ✅ 가능하면 CRUD도 worker_id로 통일 권장
    )
    if not is_owner:
        raise HTTPException(status_code=403, detail="해당 대화에 접근할 수 없습니다.")

    message = chat_crud.add_message(
        db=db,
        worker_id=current_user.worker_id,   # ✅ id → worker_id
        message_in=payload,
    )
    return message

# 3) 사용자별 대화 목록 조회
@router.get("/conversations", response_model=list[ConversationOut])
def get_my_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return chat_crud.get_conversations_by_worker(
        db=db, worker_id=current_user.worker_id
    )

# 4) 특정 대화 상세 조회 (메시지 포함)
@router.get("/conversations/{conversation_id}", response_model=ConversationWithMessages)
def get_conversation_detail(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    conversation = chat_crud.get_conversation_with_messages(
        db=db, worker_id=current_user.worker_id, conversation_id=conversation_id
    )
    return conversation

# 5) 사용자 메시지 + AI 응답 처리
@router.post("/messages/with-ai", response_model=MessageWithAIResponse)
async def handle_chat_with_ai(
    payload: MessageWithAIRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    is_owner = chat_crud.get_conversation_owner_check(
        db=db,
        conversation_id=payload.conversation_id,
        worker_id=current_user.worker_id,      # ✅ 가능하면 CRUD도 worker_id로 통일 권장
    )
    if not is_owner:
        raise HTTPException(status_code=403, detail="해당 대화에 접근할 수 없습니다.")

    user_message = chat_crud.add_message(
        db=db,
        worker_id=current_user.worker_id,    # ✅ id → worker_id
        message_in=payload,
    )

    try:
        ai_result = await call_ai_server(question=payload.content, top_k=payload.top_k)
        ai_answer = ai_result["answer"]
        ai_sources = ai_result.get("sources", [])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI 서버 호출 실패: {str(e)}")

    assistant_message = chat_crud.create_assistant_message_with_sources(
        db=db,
        worker_id=current_user.worker_id,    # ✅ id → worker_id
        conversation_id=payload.conversation_id,
        content=ai_answer,
        sources=[
            {
                "source_title": src.get("metadata", {}).get("source"),
                "source_url": None,
                "snippet": src.get("text"),
                "score": src.get("score"),
            }
            for src in ai_sources
        ],
    )

    return MessageWithAIResponse(
        message_id=assistant_message.message_id,
        content=assistant_message.content,
        sources=ai_sources,
    )
