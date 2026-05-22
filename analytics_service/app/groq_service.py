from functools import lru_cache
from pathlib import Path
import re

import httpx

from app import config


class GroqError(RuntimeError):
    pass


@lru_cache
def _load_system_prompt() -> str:
    prompts_dir = Path(__file__).resolve().parent / "prompts"
    preferred = prompts_dir / "analytics_prompt.txt"
    fallback = prompts_dir / "sql_prompt.txt"
    prompt_path = preferred if preferred.exists() else fallback
    return prompt_path.read_text(encoding="utf-8").strip()


def _extract_sql(text: str) -> str:
    fenced = re.search(r"```(?:sql)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if fenced:
        return fenced.group(1).strip()
    return text.strip()


def generate_sql(question: str) -> str:
    if not config.GROQ_API_KEY:
        raise GroqError("GROQ_API_KEY is not set")

    payload = {
        "model": config.GROQ_MODEL,
        "messages": [
            {"role": "system", "content": _load_system_prompt()},
            {"role": "user", "content": question},
        ],
        "temperature": 0.2,
        "max_tokens": 256,
    }
    headers = {"Authorization": f"Bearer {config.GROQ_API_KEY}"}

    try:
        response = httpx.post(
            config.GROQ_API_URL,
            json=payload,
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise GroqError("Groq API request failed") from exc

    data = response.json()
    content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
    sql = _extract_sql(content)
    if not sql:
        raise GroqError("Groq response did not include SQL")
    return sql
