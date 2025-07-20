from pydantic import BaseModel
from datetime import datetime
from typing import Literal


# 클라이언트 → 서버: 채팅 생성 요청
class ChatCreate(BaseModel):
    message: str
    sender: Literal["user", "bot"]


# 서버 → 클라이언트: 채팅 응답
class ChatOut(BaseModel):
    chat_id: int
    worker_id: int
    message: str
    sender: Literal["user", "bot"]
    created_at: datetime

    class Config:
        from_attributes = True  # SQLAlchemy 모델을 Pydantic 응답으로 자동 변환


#요청
class ChatInput(BaseModel):
    user_message: str
#응답
class ChatResponse(BaseModel):
    bot_message: str