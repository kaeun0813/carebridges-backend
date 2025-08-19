from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc
from app.models.chat import Conversation, Message, MessageSource
from app.schemas.chat import ConversationCreate, MessageCreate
from typing import List, Optional

# 대화 생성
def create_conversation(db: Session, worker_id: int, conversation_in: ConversationCreate) -> Conversation:
    conversation = Conversation(
        worker_id=worker_id,
        title=conversation_in.title or "새 대화"  # ✅ title 기본값 처리
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

# 특정 사용자의 대화 목록 조회
def get_conversations_by_worker(db: Session, worker_id: int) -> List[Conversation]:
    return db.query(Conversation)\
        .filter(Conversation.worker_id == worker_id)\
        .order_by(desc(Conversation.updated_at))\
        .all()

# 특정 대화 ID로 대화 + 메시지 전체 조회
def get_conversation_with_messages(db: Session, worker_id: int, conversation_id: int) -> Optional[Conversation]:
    return db.query(Conversation)\
        .options(joinedload(Conversation.messages).joinedload(Message.sources))\
        .filter(
            Conversation.worker_id == worker_id,
            Conversation.conversation_id == conversation_id
        )\
        .first()

#  메시지 저장
def add_message(db: Session, worker_id: int, message_in: MessageCreate) -> Message:
    message = Message(
        conversation_id=message_in.conversation_id,
        worker_id=worker_id,
        sender=message_in.sender.value,  # Enum -> 문자열
        content=message_in.content
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

# assistant 응답 메시지 저장 + 추가 정보 포함 (token_usage, latency, status, sources)
def create_assistant_message_with_sources(
    db: Session,
    worker_id: int,
    conversation_id: int,
    content: str,
    token_usage: int = 0,
    latency_ms: int = 0,
    status: str = "completed",
    sources: Optional[List[dict]] = None
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        worker_id=worker_id,
        sender="assistant",
        content=content,
        status=status,
        token_usage=token_usage,
        latency_ms=latency_ms
    )
    db.add(message)
    db.commit()
    db.refresh(message)

    # 출처 정보 저장
    if sources:
        for src in sources:
            source = MessageSource(
                message_id=message.message_id,
                source_title=src.get("source_title"),
                source_url=src.get("source_url"),
                snippet=src.get("snippet"),
                score=src.get("score")
            )
            db.add(source)
        db.commit()
    return message

def get_conversation_owner_check(
    db: Session, conversation_id: int, worker_id: int
) -> bool:
    """
    해당 conversation_id가 worker_id(=현재 사용자)의 소유인지 여부를 반환
    """
    return db.query(Conversation.conversation_id).filter(
        Conversation.conversation_id == conversation_id,
        Conversation.worker_id == worker_id,
    ).first() is not None