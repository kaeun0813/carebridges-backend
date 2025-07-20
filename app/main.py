from fastapi import FastAPI
from app.api.routers import router as api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"] 등 실제 허용할 도메인 (프로트 주소)
    allow_credentials=True,
    allow_methods=["*"],  # 또는 ["GET", "POST", ...]
    allow_headers=["*"],
)


# 1. HTTPException 핸들링
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

# 2. 유효성 검증 실패(RequestValidationError) 핸들링
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

# 3. 정의되지 않은 URL (404) 또는 기타 Starlette 예외
@app.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )



# 라우터 등록
app.include_router(api_router)

#루트 엔드포인트(테스트용)
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI and Poetry!"}