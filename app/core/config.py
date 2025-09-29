# app/core/config.py
from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    ENV: str = os.getenv("ENV", "dev")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    DATABASE_URL: str = os.getenv("DATABASE_URL")  # required
    HF_TOKEN: str = os.getenv("HF_TOKEN")  # required for HuggingFace
    SQL_MAX_ROWS: int = int(os.getenv("SQL_MAX_ROWS", "500"))  # safety limit

settings = Settings()
