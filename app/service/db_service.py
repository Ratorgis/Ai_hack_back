# app/services/db_service.py

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаем подключение к БД
engine = create_engine(settings.DATABASE_URL, echo=True)  # echo=True для логов SQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency для FastAPI (если понадобится)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def execute_sql(query: str):
    """
    Выполнить SQL-запрос и вернуть результат.
    :param query: SQL строка
    :return: список словарей
    """
    with engine.connect() as connection:
        result = connection.execute(text(query))
        rows = result.fetchall()
        columns = result.keys()
        data = [dict(zip(columns, row)) for row in rows]
    return data

