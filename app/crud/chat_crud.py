from sqlalchemy.orm import Session
from app.models.chat import ChatLog
from app.schemas.chat import ChatCreate
from typing import List


# 1. 대화 저장 (ChatCreate 기반)
def create_chat_log(db: Session, chat: ChatCreate, worker_id: int) -> ChatLog:
    db_chat = ChatLog(
        worker_id=worker_id,
        message=chat.message,
        sender=chat.sender
    )
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat


# 2. 대화 저장 (파라미터 기반: 사용자 메시지/봇 메시지 저장에 활용)
def save_chat(db: Session, worker_id: int, message: str, sender: str) -> ChatLog:
    new_chat = ChatLog(
        worker_id=worker_id,
        message=message,
        sender=sender
    )
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat


# 3. 특정 사용자 대화 전체 조회
def get_chat_logs_by_user(db: Session, worker_id: int) -> List[ChatLog]:
    return (
        db.query(ChatLog)
        .filter(ChatLog.worker_id == worker_id)
        .order_by(ChatLog.created_at)
        .all()
    )


# 4. 특정 사용자 최근 N개 대화 조회
def get_recent_chat_logs(db: Session, worker_id: int, limit: int = 10) -> List[ChatLog]:
    return (
        db.query(ChatLog)
        .filter(ChatLog.worker_id == worker_id)
        .order_by(ChatLog.created_at.desc())
        .limit(limit)
        .all()
    )
