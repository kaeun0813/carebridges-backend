from fastapi import FastAPI
from app.api.routers import router as api_router

app = FastAPI()

# 라우터 등록
app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI and Poetry!"}