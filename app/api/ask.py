from fastapi import APIRouter
from pydantic import BaseModel
from app.services.db_service import execute_query
from app.services.llm_service import ask_llm

router = APIRouter()

class AskRequest(BaseModel):
    question: str

@router.post("/")
async def ask(request: AskRequest):
    """
    1. Получаем вопрос пользователя (естественный язык).
    2. Преобразуем вопрос в SQL-запрос (сначала простая логика, потом LLM).
    3. Забираем данные из PostgreSQL.
    4. Отправляем данные и исходный вопрос в LLM для генерации красивого ответа.
    5. Возвращаем текст на фронт.
    """

    user_question = request.question

    # Простейший пример "ручной маппинг" вопроса → SQL
    if "сколько" in user_question.lower():
        sql = "SELECT COUNT(*) FROM some_table;"  
    else:
        sql = "SELECT * FROM some_table LIMIT 5;"  

    # 1. Выполняем SQL-запрос
    db_result = execute_query(sql)

    # 2. Отправляем вопрос + данные в LLM для красивого ответа
    llm_response = ask_llm(user_question, db_result)

    # 3. Отправляем текстовый ответ пользователю
    return {"answer": llm_response}
