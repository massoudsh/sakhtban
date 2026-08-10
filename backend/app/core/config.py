"""تنظیمات مرکزی برنامه (بارگذاری از متغیرهای محیطی)."""
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Sakhtban API"
    environment: str = "development"

    database_url: str = "postgresql+psycopg://sakhtban:sakhtban@localhost:5432/sakhtban"

    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 60 * 12

    telegram_bot_token: str | None = None
    cors_origins: list[str] = ["http://localhost:3000"]


@lru_cache
def get_settings() -> Settings:
    return Settings()
