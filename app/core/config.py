from dotenv import load_dotenv
import os

# Загружаем .env
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    HF_TOKEN: str = os.getenv("HF_TOKEN")

settings = Settings()
