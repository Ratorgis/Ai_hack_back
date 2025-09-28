import faiss
import numpy as np

# Инициализация FAISS
dimension = 384  # размерность эмбеддингов MiniLM
index = faiss.IndexFlatL2(dimension)
documents = []  # храним тексты для сопоставления

def add_document(text: str, vector: list):
    """Добавляем документ в FAISS"""
    documents.append(text)
    vec = np.array([vector]).astype("float32")
    index.add(vec)

def search(query_vector: list, top_k: int = 5):
    """Поиск ближайших векторов в FAISS"""
    vec = np.array([query_vector]).astype("float32")
    distances, indices = index.search(vec, top_k)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx < len(documents):
            results.append({
                "text": documents[idx],
                "score": float(distances[0][i])
            })
    return results
