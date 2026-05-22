import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default: str | None = None) -> str | None:
    value = os.getenv(key)
    if value is None or value == "":
        return default
    return value


DATABRICKS_MCP_URL = get_env("DATABRICKS_MCP_URL")
DATABRICKS_TOKEN = get_env("DATABRICKS_TOKEN")

GROQ_API_KEY = get_env("GROQ_API_KEY")
GROQ_MODEL = get_env("GROQ_MODEL", "llama-3.3-70b-versatile")
GROQ_API_URL = get_env("GROQ_API_URL", "https://api.groq.com/openai/v1/chat/completions")
