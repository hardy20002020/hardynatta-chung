"""add competitions table

Revision ID: cc0a17b64f6a
Revises: 569b89591841
Create Date: 2026-08-05 03:57:54.652064

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ==========================================================
# ALEMBIC REVISION
# ==========================================================

revision: str = "cc0a17b64f6a"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "569b89591841"

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
    Create the competitions table.

    This migration introduces the root competition
    entity used by future MAJE competition modules.
    """

    op.create_table(
        "competitions",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(length=200),
            nullable=False,
        ),

        sa.Column(
            "code",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "year",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default=sa.text("true"),
            nullable=False,
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f("ix_competitions_code"),
        "competitions",
        ["code"],
        unique=True,
    )

    op.create_index(
        op.f("ix_competitions_id"),
        "competitions",
        ["id"],
        unique=False,
    )


# ==========================================================
# DOWNGRADE
# ==========================================================

def downgrade() -> None:
    """
    Remove the competitions table.
    """

    op.drop_index(
        op.f("ix_competitions_id"),
        table_name="competitions",
    )

    op.drop_index(
        op.f("ix_competitions_code"),
        table_name="competitions",
    )

    op.drop_table(
        "competitions",
    )