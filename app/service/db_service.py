# app/services/db_service.py
import re
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаём движок
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Простая валидация SQL — разрешаем только SELECT / WITH ... SELECT
_forbidden_pattern = re.compile(
    r'\b(DROP|DELETE|INSERT|UPDATE|ALTER|TRUNCATE|CREATE|GRANT|REVOKE|SHUTDOWN)\b',
    flags=re.IGNORECASE
)

def _validate_sql(sql: str):
    sql_stripped = sql.strip()
    # Запрещаем множественные инструкций (точка с запятой)
    if ';' in sql_stripped.replace('\\;', ''):
        raise ValueError("Multiple statements or semicolon found — disallowed for safety.")
    # Запрещаем опасные ключевые слова
    if _forbidden_pattern.search(sql):
        raise ValueError("Detected forbidden SQL operation (DDL/DML). Only SELECT allowed.")
    # Основное требование — должен быть SELECT или WITH ... SELECT
    if not re.match(r'^(WITH\s+.*\s+)?SELECT\b', sql_stripped, flags=re.IGNORECASE|re.DOTALL):
        raise ValueError("Only SELECT queries are allowed.")
    return True

def execute_sql(sql: str, max_rows: int = None):
    """
    Выполнить безопасный SELECT SQL и вернуть список словарей.
    """
    if max_rows is None:
        max_rows = settings.SQL_MAX_ROWS

    _validate_sql(sql)

    # Добавим LIMIT если в запросе его нет, чтобы защититься
    if not re.search(r'\bLIMIT\b', sql, flags=re.IGNORECASE):
        sql = f"{sql.rstrip()} LIMIT {max_rows}"

    with engine.connect() as conn:
        result = conn.execute(text(sql))
        rows = result.fetchall()
        keys = result.keys()
        data = [dict(zip(keys, row)) for row in rows]
    return data
