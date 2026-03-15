"""Centralised settings using pydantic-settings.

All configuration is read from environment variables (or a .env file).
Never hard-code secrets — use the .env.example file as a reference.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # Application
    APP_NAME: str = "Predictive Analytics API"
    APP_VERSION: str = "0.1.0"
    ENV: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://pa_user:pa_pass@localhost:5432/pa_db"

    # MLflow
    MLFLOW_TRACKING_URI: str = "http://localhost:5001"

    # Models
    MODELS_DIR: str = "models"

    @property
    def is_development(self) -> bool:
        return self.ENV == "development"


# Module-level singleton — import this everywhere
settings = Settings()
