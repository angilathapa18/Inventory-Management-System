from pathlib import Path
from typing import Self
from urllib.parse import quote_plus

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Option A: full URL
    database_url: str | None = None

    # Option B: individual fields (from Supabase Session pooler)
    db_host: str | None = None
    db_port: int = 5432
    db_name: str = "postgres"
    db_user: str | None = None
    db_password: str | None = None

    database_ssl: bool = False
    database_ssl_verify: bool = True
    cors_origins: list[str] = ["http://localhost:3000"]

    @model_validator(mode="after")
    def resolve_database_url(self) -> Self:
        if self.database_url:
            url = self.database_url
        elif self.db_host and self.db_user and self.db_password:
            password = quote_plus(self.db_password)
            url = (
                f"postgresql+asyncpg://{self.db_user}:{password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        else:
            url = "postgresql+asyncpg://postgres:postgres@localhost:5432/inventory"

        if url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)

        self.database_url = url
        return self


settings = Settings()
