import httpx
from app.core.config import settings

async def call_ai_server(question: str, top_k: int = 5) -> dict:
    """
    AI 서버에 질문을 보내고 응답을 받습니다.

    Parameters:
    - question (str): 사용자 질문
    - top_k (int): RAG에서 검색할 문서 수

    Returns:
    - dict: {"answer": ..., "sources": [...]}
    """
    payload = {"question": question, "top_k": top_k}
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(str(settings.AI_SERVER_URL), json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"[AI 서버 오류] 상태 코드 {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise RuntimeError(f"[AI 서버 호출 실패] {str(e)}")
