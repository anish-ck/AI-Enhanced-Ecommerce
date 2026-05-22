import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default: str | None = None) -> str | None:
    value = os.getenv(key)
    return value if value is not None else default


DATABASE_URL = get_env(
    "DATABASE_URL",
    "postgresql://postgres:password@postgres:5432/ecommerce_db",
)
SECRET_KEY = get_env("SECRET_KEY", "change_me")
ALGORITHM = get_env("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(get_env("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

origins_raw = get_env("CORS_ORIGINS", "http://localhost:5173")
CORS_ORIGINS = [item.strip() for item in origins_raw.split(",") if item.strip()]

EVENT_HUB_BOOTSTRAP_SERVER = get_env("EVENT_HUB_BOOTSTRAP_SERVER")
EVENT_HUB_CONNECTION_STRING = get_env("EVENT_HUB_CONNECTION_STRING")
EVENT_HUB_TOPIC = get_env("EVENT_HUB_TOPIC")
OLLAMA_URL = get_env("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = get_env("OLLAMA_MODEL", "qwen3-vl:8b")
ANALYTICS_SERVICE_URL = get_env("ANALYTICS_SERVICE_URL", "http://analytics_service:8001")
