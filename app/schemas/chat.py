from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


# 발신자 구분
class SenderEnum(str, Enum):
    user = "user"
    assistant = "assistant"


# 메시지 상태
class MessageStatus(str, Enum):
    saved = "saved"
    completed = "completed"
    failed = "failed"


# RAG 출처 정보
class MessageSourceOut(BaseModel):
    source_title: Optional[str]
    source_url: Optional[str]
    snippet: Optional[str]
    score: Optional[float]
    created_at: Optional[datetime]

    class Config:
        from_attributes = True


# 메시지 응답용 스키마
class MessageOut(BaseModel):
    message_id: int
    conversation_id: int
    worker_id: int
    sender: SenderEnum
    content: str
    status: MessageStatus
    token_usage: int
    latency_ms: int
    created_at: datetime
    updated_at: datetime
    sources: Optional[List[MessageSourceOut]] = []

    class Config:
        from_attributes = True


# 메시지 생성 요청용
class MessageCreate(BaseModel):
    conversation_id: int
    sender: SenderEnum
    content: str


# 대화 생성 요청용
class ConversationCreate(BaseModel):
    title: Optional[str] = None


# 대화 응답용
class ConversationOut(BaseModel):
    conversation_id: int
    worker_id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 단일 대화 + 메시지 전체 조회
class ConversationWithMessages(BaseModel):
    conversation_id: int
    worker_id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime
    messages: List[MessageOut]

    class Config:
        from_attributes = True


class MessageWithAIRequest(MessageCreate):
    top_k: int = 3

class MessageWithAIResponse(BaseModel):
    message_id: int
    content: str
    sources: list[dict]  # 추후 SourceResponse 스키마로 정리 가능
