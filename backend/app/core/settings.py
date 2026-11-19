"""Application settings.

Environment-driven configuration only. No hardcoded credentials, hostnames or
URLs. Production uses a separate environment configuration (Stage C).
"""

from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Mini EMS"
    app_env: str = Field(default="development", alias="APP_ENV")
    app_debug: bool = Field(default=True, alias="APP_DEBUG")
    api_host: str = Field(default="127.0.0.1", alias="API_HOST")
    api_port: int = Field(default=8000, alias="API_PORT")
    database_url: str | None = Field(default=None, alias="DATABASE_URL")
    test_database_url: str | None = Field(default=None, alias="TEST_DATABASE_URL")
    test_database_host: str | None = Field(default=None, alias="TEST_DATABASE_HOST")
    frontend_url: str = Field(default="http://localhost:5173", alias="FRONTEND_URL")

    @field_validator("app_env")
    @classmethod
    def validate_app_env(cls, v: str) -> str:
        allowed = {"development", "testing", "production"}
        if v not in allowed:
            raise ValueError(f"APP_ENV must be one of {sorted(allowed)}")
        return v

    @field_validator("database_url", "test_database_url")
    @classmethod
    def validate_database_url(cls, v: str | None) -> str | None:
        if v is None:
            return v
        if not v.startswith("postgresql+psycopg://"):
            raise ValueError("DATABASE_URL must use the postgresql+psycopg:// scheme")
        return v


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance (FastAPI dependency)."""
    return Settings()
