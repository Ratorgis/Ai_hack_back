from fastapi import FastAPI
from app.api import health
from app.core.config import settings

app = FastAPI(title=settings.PROJECT_NAME)

# Routers
app.include_router(health.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI_Search_Backend is running"}
