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
