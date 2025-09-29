# app/api/ask.py

from fastapi import APIRouter
from pydantic import BaseModel
from app.services import llm_service, db_service

router = APIRouter()

class AskRequest(BaseModel):
    query: str

@router.post("/ask")
def ask(request: AskRequest):
    # 1. Получаем SQL от LLM
    sql_query = llm_service.nl2sql(request.query)

    # 2. Выполняем запрос в БД
    try:
        results = db_service.execute_sql(sql_query)
    except Exception as e:
        return {"error": str(e), "sql_query": sql_query}

    # 3. Возвращаем SQL и данные
    return {
        "natural_query": request.query,
        "sql_query": sql_query,
        "results": results
    }
