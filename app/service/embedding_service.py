from sentence_transformers import SentenceTransformer

# Используем бесплатную модель эмбеддингов
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed_text(text: str):
    """Преобразуем текст в вектор"""
    return model.encode(text).tolist()
