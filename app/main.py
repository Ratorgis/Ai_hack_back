from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import ask
from app.api import health

# Инициализация приложения FastAPI
app = FastAPI(title="AI Search Backend", version="1.0")

# Настраиваем CORS (чтобы фронтенд на HTML/JS мог обращаться к API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # в проде лучше указывать конкретный фронт-домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(health.router, prefix="/api/health", tags=["health"])
app.include_router(ask.router, prefix="/api/ask", tags=["ask"])
