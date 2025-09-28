from fastapi import APIRouter, UploadFile, File
from app.services import embedding_service, search_service

router = APIRouter()

@router.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    """
    Загружаем текстовый файл, режем на строки и добавляем в FAISS
    """
    content = (await file.read()).decode("utf-8")
    lines = content.split("\n")

    for line in lines:
        if line.strip():
            vector = embedding_service.embed_text(line)
            search_service.add_document(line, vector)

    return {"status": "ok", "ingested": len(lines)}
