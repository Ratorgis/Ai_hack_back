from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Search Backend"
    DATABASE_URL: str = "postgresql://app:changeme@localhost:5432/ai_search"

settings = Settings()
