import pytest
from pydantic import ValidationError

from app.core.config import Settings


def make_settings(**overrides):
    values = {
        "ENVIRONMENT": "development",
        "DEBUG": True,
        "JWT_SECRET_KEY":
            "development-only-change-this-secret",
    }
    values.update(overrides)

    return Settings(
        _env_file=None,
        **values,
    )


def test_development_defaults_remain_allowed():
    settings = make_settings()

    assert settings.ENVIRONMENT == "development"
    assert settings.DEBUG is True


def test_production_rejects_debug_mode():
    with pytest.raises(
        ValidationError,
        match="DEBUG must be False in production",
    ):
        make_settings(
            ENVIRONMENT="production",
            DEBUG=True,
            JWT_SECRET_KEY=(
                "MAJE-Production-Secure-Secret-"
                "2026-Enterprise"
            ),
        )


@pytest.mark.parametrize(
    "secret",
    [
        "",
        "development-only-change-this-secret",
        "replace-with-a-strong-secret",
    ],
)
def test_production_rejects_insecure_jwt_secret(
    secret,
):
    with pytest.raises(
        ValidationError,
        match=(
            "A secure JWT_SECRET_KEY is required "
            "in production"
        ),
    ):
        make_settings(
            ENVIRONMENT="production",
            DEBUG=False,
            JWT_SECRET_KEY=secret,
        )


def test_production_accepts_secure_configuration():
    settings = make_settings(
        ENVIRONMENT="production",
        DEBUG=False,
        JWT_SECRET_KEY=(
            "MAJE-Production-Secure-Secret-"
            "2026-Enterprise"
        ),
        DATABASE_URL=(
            "postgresql+psycopg://"
            "maje_app:StrongDatabasePassword2026!"
            "@db.internal:5432/maje"
        ),
        CORS_ALLOWED_ORIGINS=(
            "https://app.maje.example.com"
        ),
        ALLOWED_HOSTS="api.maje.example.com",
    )

    assert settings.ENVIRONMENT == "production"
    assert settings.DEBUG is False


def test_production_rejects_short_jwt_secret():
    with pytest.raises(
        ValidationError,
        match=(
            "JWT_SECRET_KEY must be at least "
            "32 characters in production"
        ),
    ):
        make_settings(
            ENVIRONMENT="production",
            DEBUG=False,
            JWT_SECRET_KEY="Short-Secret-2026!",
        )


def test_production_rejects_default_database_credentials():
    with pytest.raises(
        ValidationError,
        match=(
            "Default database credentials "
            "are not allowed in production"
        ),
    ):
        make_settings(
            ENVIRONMENT="production",
            DEBUG=False,
            JWT_SECRET_KEY=(
                "MAJE-Production-Secure-Secret-"
                "2026-Enterprise"
            ),
            DATABASE_URL=(
                "postgresql+psycopg://"
                "postgres:postgres@localhost:5432/maje"
            ),
        )


def test_production_accepts_secure_database_credentials():
    settings = make_settings(
        ENVIRONMENT="production",
        DEBUG=False,
        JWT_SECRET_KEY=(
            "MAJE-Production-Secure-Secret-"
            "2026-Enterprise"
        ),
        DATABASE_URL=(
            "postgresql+psycopg://"
            "maje_app:StrongDatabasePassword2026!"
            "@db.internal:5432/maje"
        ),
        CORS_ALLOWED_ORIGINS=(
            "https://app.maje.example.com"
        ),
        ALLOWED_HOSTS="api.maje.example.com",
    )

    assert settings.ENVIRONMENT == "production"


def test_production_rejects_development_cors_origins():
    with pytest.raises(
        ValidationError,
        match=(
            "Development CORS origins are not "
            "allowed in production"
        ),
    ):
        make_settings(
            ENVIRONMENT="production",
            DEBUG=False,
            JWT_SECRET_KEY=(
                "MAJE-Production-Secure-Secret-"
                "2026-Enterprise"
            ),
            DATABASE_URL=(
                "postgresql+psycopg://"
                "maje_app:StrongDatabasePassword2026!"
                "@db.internal:5432/maje"
            ),
            CORS_ALLOWED_ORIGINS=(
                "http://localhost:5173"
            ),
            ALLOWED_HOSTS="api.maje.example.com",
        )


def test_production_rejects_development_trusted_hosts():
    with pytest.raises(
        ValidationError,
        match=(
            "Development trusted hosts are not "
            "allowed in production"
        ),
    ):
        make_settings(
            ENVIRONMENT="production",
            DEBUG=False,
            JWT_SECRET_KEY=(
                "MAJE-Production-Secure-Secret-"
                "2026-Enterprise"
            ),
            DATABASE_URL=(
                "postgresql+psycopg://"
                "maje_app:StrongDatabasePassword2026!"
                "@db.internal:5432/maje"
            ),
            CORS_ALLOWED_ORIGINS=(
                "https://app.maje.example.com"
            ),
            ALLOWED_HOSTS="localhost",
        )


def test_production_accepts_secure_cors_and_hosts():
    settings = make_settings(
        ENVIRONMENT="production",
        DEBUG=False,
        JWT_SECRET_KEY=(
            "MAJE-Production-Secure-Secret-"
            "2026-Enterprise"
        ),
        DATABASE_URL=(
            "postgresql+psycopg://"
            "maje_app:StrongDatabasePassword2026!"
            "@db.internal:5432/maje"
        ),
        CORS_ALLOWED_ORIGINS=(
            "https://app.maje.example.com"
        ),
        ALLOWED_HOSTS="api.maje.example.com",
    )

    assert settings.cors_allowed_origins == [
        "https://app.maje.example.com"
    ]

    assert settings.allowed_hosts == [
        "api.maje.example.com"
    ]
