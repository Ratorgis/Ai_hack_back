from fastapi import APIRouter
from pydantic import BaseModel
from app.services import search_service, llm_service

router = APIRouter()

class AskRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/ask")
async def ask_docs(request: AskRequest):
    # 1. Получаем релевантные куски текста из FAISS
    results = search_service.search(request.query, request.top_k)

    # 2. Собираем контекст
    context = "\n".join([r["text"] for r in results])

    # 3. Отправляем в HuggingFace LLM
    answer = llm_service.generate_answer(context, request.query)

    return {
        "query": request.query,
        "answer": answer,
        "sources": results
    }
