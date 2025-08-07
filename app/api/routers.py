from fastapi import APIRouter
from app.api.endpoints import user, auth, chat, faq # 여기서 guide도 나중에 추가 가능

router = APIRouter()

# 각 기능별 라우터 등록
router.include_router(user.router, prefix="/auth", tags=["User"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(chat.router, prefix="/chat", tags=["Chat"])
router.include_router(faq.router, prefix="/faq", tags=["FAQ"])