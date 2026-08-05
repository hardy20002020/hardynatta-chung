from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from app.core.config import settings
from app.db.base import Base

# Load semua model agar Alembic mengenali metadata
from app.models import (
    User,
    Province,
    City,
    Role,
    Permission,
    RolePermission,
    AuditLog,
    UserSession,
    Competition,
    CompetitionGroup,
    ChineseSurname,
    ChineseSurnameAlias,
    Ethnicity,
    Participant,
)


# Alembic Config object
config = context.config


# Set database URL dari settings
config.set_main_option(
    "sqlalchemy.url",
    settings.DATABASE_URL,
)


# Setup logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata untuk autogenerate migration
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations in offline mode.
    """

    url = config.get_main_option(
        "sqlalchemy.url"
    )

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in online mode.
    """

    connectable = engine_from_config(
        config.get_section(
            config.config_ini_section,
            {},
        ),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()