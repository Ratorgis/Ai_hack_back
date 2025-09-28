import os
from app.utils.text_splitter import split_text
from app.services.embeddings import add_to_index

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def process_file(file_path: str):
    """
    Обработка файла: читаем, разбиваем на чанки, сохраняем эмбеддинги.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # Разбиваем на чанки
    chunks = split_text(text)

    # Сохраняем в FAISS
    added = add_to_index(chunks)

    return {"chunks": len(chunks), "added": added}
