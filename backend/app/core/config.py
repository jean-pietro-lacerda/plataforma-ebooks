from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str | None = None
    migrations_database_url: str | None = None

    news_upload_dir: str = "/workspace/storage/uploads"

    jwt_secret_key: str | None = None
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=(Path("/workspace/.env"), Path(__file__).resolve().parents[3] / ".env"),
        env_file_encoding="utf-8-sig",
        env_ignore_empty=True,
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()