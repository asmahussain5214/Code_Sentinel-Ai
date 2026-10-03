from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration settings loaded from environment variables."""

    APP_NAME: str = "CodeSentinel AI"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Database Settings
    DB_USER: str = "codesentinel_user"
    DB_PASSWORD: str = "password"
    DB_HOST: str = "localhost"
    DB_PORT: int = 1521
    DB_SERVICE_NAME: str = "FREEPDB1"

    # JWT Settings
    SECRET_KEY: str = "default_dev_secret"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # LLM Settings
    LLM_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file="backend/.env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()