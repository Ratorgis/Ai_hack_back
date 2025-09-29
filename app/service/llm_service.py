from app.core.config import settings
from huggingface_hub import InferenceClient

# Подключаем клиент HuggingFace Inference API
client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",  # можно заменить на другую модель
    token=settings.HF_TOKEN
)

def generate_answer(context: str, query: str) -> str:
    """
    Формируем промпт и отправляем в HuggingFace LLM.
    """
    prompt = f"""
Ты — корпоративный ассистент. Отвечай только на основе приведённого контекста.

Контекст:
{context}

Вопрос:
{query}

Ответ должен быть ясным, кратким и по существу.
"""

    try:
        response = client.text_generation(
            prompt,
            max_new_tokens=400,
            temperature=0.2,
            do_sample=True  # включаем вероятностный выбор для разнообразия
        )
        return response.strip()
    except Exception as e:
        return f"Ошибка при генерации ответа: {e}"
