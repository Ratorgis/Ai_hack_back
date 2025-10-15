from transformers import pipeline
from app.config import settings

# Используем HF pipeline для генерации текста
generator = pipeline(
    "text-generation",
    model=settings.HF_MODEL,
    use_auth_token=settings.HF_TOKEN
)

def ask_llm(question: str, context: str):
    prompt = f"Вопрос: {question}\nДанные: {context}\nСформируй понятный ответ:"
    result = generator(prompt, max_length=300, do_sample=True)
    return result[0]['generated_text']

def generate_answer(question: str, data: list[dict]):
    """
    question: исходный вопрос пользователя
    data: данные из базы, которые нужно красиво оформить
    """
    # Формируем текстовый контекст
    data_text = "\n".join([str(row) for row in data]) or "Нет данных"
    prompt = f"Вопрос: {question}\nДанные: {data_text}\nОтвет:"

    result = llm_pipeline(prompt, max_length=512, do_sample=False)
    return result[0]['generated_text']