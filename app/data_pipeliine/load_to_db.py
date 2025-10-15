import os
import psycopg2
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения (.env)
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:your_password@localhost:5432/your_db")

def load_csv_to_db(csv_dir="./dataset_raw"):
    """ Загружаем все CSV из папки dataset_raw в PostgreSQL """
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    csv_dir = Path(csv_dir)
    for csv_file in csv_dir.glob("*.csv"):
        table_name = csv_file.stem  # имя таблицы = имя файла
        df = pd.read_csv(csv_file)

        # Удаляем таблицу если существует (для чистой перезагрузки)
        cur.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE")

        # Создаём таблицу
        columns = ", ".join([f"{col} TEXT" for col in df.columns])
        cur.execute(f"CREATE TABLE {table_name} ({columns})")

        # Загружаем данные в PostgreSQL
        for _, row in df.iterrows():
            values = "', '".join(str(v).replace("'", "''") for v in row.values)
            cur.execute(f"INSERT INTO {table_name} VALUES ('{values}')")

        print(f"Загружена таблица {table_name}, строк: {len(df)}")

    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    load_csv_to_db()
