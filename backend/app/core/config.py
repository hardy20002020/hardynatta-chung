from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


class Settings(BaseSettings):

    # ==========================================================
    # APPLICATION
    # ==========================================================

    APP_NAME: str = "MAJE API"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True


    # ==========================================================
    # DATABASE
    # ==========================================================

    DATABASE_URL: str = (
        "postgresql+psycopg://"
        "postgres:postgres@localhost:5432/maje"
    )


    # ==========================================================
    # JWT SECURITY
    # ==========================================================

    JWT_SECRET_KEY: str = (
        "development-only-change-this-secret"
    )

    JWT_ALGORITHM: str = "HS256"

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60


    # ==========================================================
    # SETTINGS
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()