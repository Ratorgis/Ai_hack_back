from fastapi import APIRouter, HTTPException, Query
from app.services.db_service import execute_query
from app.services.llm_service import generate_answer
import asyncio

router = APIRouter()

@router.get("/ask")
async def ask(question: str = Query(..., description="Ваш вопрос на естественном языке")):
    """
    1. Преобразуем вопрос в SQL
    2. Получаем данные из базы
    3. Генерируем красивый ответ через LLM
    4. Возвращаем на фронт
    """
    # Простейшая логика преобразования вопроса в SQL
    # Например: "Сколько пользователей?" → "SELECT COUNT(*) FROM users;"
    if "сколько пользователей" in question.lower():
        sql = "SELECT COUNT(*) as count FROM users;"
    else:
        # Для сложных вопросов позже можно подключить LLM для генерации SQL
        sql = "SELECT * FROM users LIMIT 10;"  

    # Получаем данные из PostgreSQL
    try:
        data = await execute_query(sql)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка базы данных: {e}")

    # Генерируем ответ через LLM
    answer = generate_answer(question, data)

    return {"question": question, "answer": answer, "data": data}
