from fastapi import FastAPI
from app.api import health, ingest, search, ask
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Routers
app.include_router(health.router, prefix = "/api")
app.include_router(ingest.router, prefix = '/api')
app.include_router(search.router, prefix = '/api')
app.include_router(ask.router, prefix = '/api')

@app.get("/")
def root():
    return {"message": "AI_Search_Backend is running"}
