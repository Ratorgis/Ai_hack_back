import asyncpg
from app.config import settings

async def execute_query(sql: str):
    conn = await asyncpg.connect(settings.DATABASE_URL)
    try:
        result = await conn.fetch(sql)
        # Преобразуем в список словарей
        return [dict(record) for record in result]
    finally:
        await conn.close()
