# app/services/llm_service.py
from app.core.config import settings
from huggingface_hub import InferenceClient
import textwrap

client = InferenceClient(model=settings.HF_MODEL, token=settings.HF_TOKEN)

def _clean_response_text(resp):
    # API может возвращать dict/str depending on client; handle both
    if isinstance(resp, str):
        return resp.strip()
    if isinstance(resp, dict):
        # For many HF clients text_generation returns dict with 'generated_text' or list
        if 'generated_text' in resp:
            return resp['generated_text'].strip()
        # fallback: try to stringify
        return str(resp).strip()
    return str(resp).strip()

def nl2sql(natural_query: str, schema_hint: str = "") -> str:
    """
    Превращает NL запрос в SQL. Возвращает строку с SQL.
    schema_hint — краткое описание таблиц/полей (рекомендуется передавать).
    """
    prompt = textwrap.dedent(f"""
    You are an expert SQL generator. Given a user's request in natural language, produce a single, valid PostgreSQL SELECT query only.
    Do NOT provide any commentary or explanation — return only the SQL.
    If you need to reference schema, use this hint:
    {schema_hint}

    User request:
    {natural_query}

    Return only one SELECT query (no explanations). Use table/column names as in the schema hint.
    """).strip()

    resp = client.text_generation(prompt, max_new_tokens=256, temperature=0.0)
    sql = _clean_response_text(resp)
    # Heuristics: if model outputs code fences, strip them
    sql = sql.strip("` \n")
    return sql

def generate_answer(natural_query: str, sql_query: str, rows: list) -> str:
    """
    Генерирует user-friendly текстовый ответ, опираясь на исполненный SQL и полученные строки.
    rows — список словарей (результат execute_sql)
    """
    # Prepare a concise table preview
    preview = ""
    if not rows:
        preview = "Записей не найдено."
    else:
        # show up to 10 rows as small table
        max_preview = 10
        cols = list(rows[0].keys())
        header = " | ".join(cols)
        preview_lines = [header]
        for r in rows[:max_preview]:
            row_line = " | ".join(str(r.get(c, "")) for c in cols)
            preview_lines.append(row_line)
        preview = "\n".join(preview_lines)
        if len(rows) > max_preview:
            preview += f"\n... (всего {len(rows)} строк, показано {max_preview})"

    prompt = textwrap.dedent(f"""
    You are an assistant that summarizes SQL query results for end users in concise human-readable language.
    User asked: {natural_query}

    Executed SQL:
    {sql_query}

    Query result (preview):
    {preview}

    Provide:
    1) A short natural-language summary answering the user's question based only on the data above.
    2) If appropriate, mention how many rows matched.
    3) Do not hallucinate facts not present in the preview.
    Return the summary in Russian (or same language as user) and be concise.
    """).strip()

    resp = client.text_generation(prompt, max_new_tokens=300, temperature=0.0)
    answer = _clean_response_text(resp)
    return answer
