import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class Settings(BaseSettings):
    PROJECT_NAME: str = "CodeSentinel AI"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "change-this-development-secret-key",
    )

    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "sqlite:///./codesentinel.db",
    )

    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()