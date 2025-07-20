from fastapi import FastAPI
from app.api.routers import router as api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"] 등 실제 허용할 도메인 (프로트 주소)
    allow_credentials=True,
    allow_methods=["*"],  # 또는 ["GET", "POST", ...]
    allow_headers=["*"],
)


# 라우터 등록
app.include_router(api_router)

#루트 엔드포인트(테스트용)
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI and Poetry!"}