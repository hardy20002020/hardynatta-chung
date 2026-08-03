"""baseline

Revision ID: 9e57bf247ab5
Revises:
Create Date: 2026-07-26 06:25:06.073832

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ==========================================================
# ALEMBIC REVISION
# ==========================================================

revision: str = "9e57bf247ab5"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = None

branch_labels: Union[
    str,
    Sequence[str],
    None,
] = None

depends_on: Union[
    str,
    Sequence[str],
    None,
] = None


# ==========================================================
# UPGRADE
# ==========================================================

def upgrade() -> None:
    """
    Create the original MAJE core schema.

    This baseline represents the schema that existed
    before the later RBAC and security migrations.

    Columns introduced by later migrations are
    intentionally excluded.
    """

    # ======================================================
    # PROVINCES
    # ======================================================

    op.create_table(
        "provinces",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.UniqueConstraint(
            "name"
        ),
    )

    op.create_index(
        op.f("ix_provinces_id"),
        "provinces",
        ["id"],
        unique=False,
    )


    # ======================================================
    # CITIES
    # ======================================================

    op.create_table(
        "cities",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "province_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),

        sa.ForeignKeyConstraint(
            ["province_id"],
            ["provinces.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),
    )

    op.create_index(
        op.f("ix_cities_id"),
        "cities",
        ["id"],
        unique=False,
    )


    # ======================================================
    # USERS
    # ======================================================

    op.create_table(
        "users",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "email",
            sa.String(),
            nullable=False,
        ),

        sa.Column(
            "password",
            sa.String(),
            nullable=False,
        ),

        # Legacy role column.
        #
        # This column existed before the RBAC migration.
        # Migration 274ddaa6bf75 removes it after role_id
        # becomes the authoritative user-role reference.

        sa.Column(
            "role",
            sa.String(length=50),
            server_default=sa.text("'user'"),
            nullable=False,
        ),

        sa.Column(
            "province_id",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "city_id",
            sa.Integer(),
            nullable=True,
        ),

        sa.ForeignKeyConstraint(
            ["province_id"],
            ["provinces.id"],
        ),

        sa.ForeignKeyConstraint(
            ["city_id"],
            ["cities.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id"
        ),

        sa.UniqueConstraint(
            "email"
        ),
    )

    op.create_index(
        op.f("ix_users_id"),
        "users",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_users_email"),
        "users",
        ["email"],
        unique=True,
    )


# ==========================================================
# DOWNGRADE
# ==========================================================

def downgrade() -> None:
    """
    Remove the original MAJE core schema.

    Tables are removed in reverse foreign-key order.
    """

    # ======================================================
    # USERS
    # ======================================================

    op.drop_index(
        op.f("ix_users_email"),
        table_name="users",
    )

    op.drop_index(
        op.f("ix_users_id"),
        table_name="users",
    )

    op.drop_table(
        "users"
    )


    # ======================================================
    # CITIES
    # ======================================================

    op.drop_index(
        op.f("ix_cities_id"),
        table_name="cities",
    )

    op.drop_table(
        "cities"
    )


    # ======================================================
    # PROVINCES
    # ======================================================

    op.drop_index(
        op.f("ix_provinces_id"),
        table_name="provinces",
    )

    op.drop_table(
        "provinces"
    )