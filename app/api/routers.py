from fastapi import APIRouter
from app.api.endpoints import user, auth  # 여기서 chat, guide도 나중에 추가 가능

router = APIRouter()

# 각 기능별 라우터 등록
router.include_router(user.router, prefix="/auth", tags=["User"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])