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

    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


    # ==========================================================
    # CORS SECURITY
    # ==========================================================

    CORS_ALLOWED_ORIGINS: str = (
        "http://localhost:5173,"
        "http://localhost:5174"
    )

    CORS_ALLOWED_METHODS: str = (
        "GET,POST,PUT,DELETE,OPTIONS"
    )

    CORS_ALLOWED_HEADERS: str = (
        "Authorization,Content-Type"
    )


    @property
    def cors_allowed_origins(self) -> list[str]:
        return [
            origin.strip()
            for origin
            in self.CORS_ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]


    @property
    def cors_allowed_methods(self) -> list[str]:
        return [
            method.strip()
            for method
            in self.CORS_ALLOWED_METHODS.split(",")
            if method.strip()
        ]


    @property
    def cors_allowed_headers(self) -> list[str]:
        return [
            header.strip()
            for header
            in self.CORS_ALLOWED_HEADERS.split(",")
            if header.strip()
        ]


    # ==========================================================
    # RATE LIMIT SECURITY
    # ==========================================================

    LOGIN_RATE_LIMIT: str = "5/minute"


    # ==========================================================
    # ACCOUNT LOCKOUT SECURITY
    # ==========================================================

    MAX_FAILED_LOGIN_ATTEMPTS: int = 5

    ACCOUNT_LOCKOUT_MINUTES: int = 15


    # ==========================================================
    # TRUSTED HOST SECURITY
    # ==========================================================

    ALLOWED_HOSTS: str = (
        "localhost,"
        "127.0.0.1,"
        "testserver"
    )


    @property
    def allowed_hosts(self) -> list[str]:
        return [
            host.strip()
            for host
            in self.ALLOWED_HOSTS.split(",")
            if host.strip()
        ]


    # ==========================================================
    # SETTINGS
    # ==========================================================

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()