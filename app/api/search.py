from fastapi import APIRouter
from pydantic import BaseModel
from app.services import embedding_service, search_service

router = APIRouter()

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

@router.post("/search")
async def search_docs(request: SearchRequest):
    """Простой поиск по FAISS"""
    query_vec = embedding_service.embed_text(request.query)
    results = search_service.search(query_vec, request.top_k)
    return {"query": request.query, "results": results}
