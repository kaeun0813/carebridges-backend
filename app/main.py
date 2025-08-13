from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.api.routers import router as api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["http://localhost:3000"] 등 실제 허용할 도메인 (프로트 주소)
    allow_credentials=True,
    allow_methods=["*"],  # 또는 ["GET", "POST", ...]
    allow_headers=["*"],
)

def build_error_response(message: str, errors: list[dict] | None = None, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={"message": message, "errors": errors or []},
    )

# 422: Pydantic 검증 에러 -> 일관 포맷으로 변환
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for e in exc.errors():
        loc = e.get("loc", [])
        # loc 예: ["body","password2"]
        field = loc[-1] if loc else None
        errors.append({
            "field": field,
            "message": e.get("msg"),
            "code": e.get("type"),
        })
    return build_error_response("유효성 검증 실패", errors, status_code=422)

# 애플리케이션에서 raise HTTPException 한 경우
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict):
        message = exc.detail.get("message", "요청 처리 중 오류가 발생했습니다.")
        errors = exc.detail.get("errors", [])
    else:
        message = str(exc.detail)
        errors = []
    return build_error_response(message, errors, status_code=exc.status_code)

# Starlette 레벨 예외 (404 등)
@app.exception_handler(StarletteHTTPException)
async def starlette_exception_handler(request: Request, exc: StarletteHTTPException):
    message = exc.detail if isinstance(exc.detail, str) else "요청 처리 중 오류가 발생했습니다."
    return build_error_response(message, [], status_code=exc.status_code)

# 라우터 등록
app.include_router(api_router)

# 헬스체크
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI and Poetry!"}
