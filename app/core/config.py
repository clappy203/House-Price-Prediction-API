"""Application configuration.

Settings are read from environment variables (prefixed ``APP_``) or an optional
``.env`` file, so the same code runs unchanged across local, CI, and production.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Strongly-typed application settings."""

    # ``protected_namespaces=()`` allows fields named ``model_*`` without warnings.
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        extra="ignore",
        protected_namespaces=(),
    )

    app_name: str = "House Price Prediction API"
    environment: str = Field(default="development")
    log_level: str = Field(default="INFO")

    #: Filesystem path to the serialized model artifact.
    model_path: Path = Field(default=Path("artifacts/model.joblib"))

    #: Allowed CORS origins. Tighten this in production.
    cors_origins: list[str] = Field(default_factory=lambda: ["*"])


@lru_cache
def get_settings() -> Settings:
    """Return a cached :class:`Settings` instance."""
    return Settings()
