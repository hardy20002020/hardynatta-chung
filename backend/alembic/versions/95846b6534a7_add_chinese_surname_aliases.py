"""add chinese surname aliases

Revision ID: 95846b6534a7
Revises: 93ebeef75e2a
Create Date: 2026-08-05 06:42:03.642402

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ==========================================================
# ALEMBIC REVISION
# ==========================================================

revision: str = "95846b6534a7"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "93ebeef75e2a"

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
    Create Chinese surname alias master data.

    Multiple character variants can reference
    one canonical Chinese surname.

    Example:

        鍾
        锺
        钟

    can all reference the same ChineseSurname.
    """

    op.create_table(
        "chinese_surname_aliases",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "chinese_surname_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "character",
            sa.String(length=10),
            nullable=False,
        ),

        sa.Column(
            "variant_type",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "is_primary",
            sa.Boolean(),
            server_default=sa.text("false"),
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

        sa.ForeignKeyConstraint(
            ["chinese_surname_id"],
            ["chinese_surnames.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f(
            "ix_chinese_surname_aliases_"
            "character"
        ),
        "chinese_surname_aliases",
        ["character"],
        unique=True,
    )

    op.create_index(
        op.f(
            "ix_chinese_surname_aliases_"
            "chinese_surname_id"
        ),
        "chinese_surname_aliases",
        ["chinese_surname_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_chinese_surname_aliases_id"
        ),
        "chinese_surname_aliases",
        ["id"],
        unique=False,
    )


# ==========================================================
# DOWNGRADE
# ==========================================================

def downgrade() -> None:
    """
    Remove Chinese surname alias master data.
    """

    op.drop_index(
        op.f(
            "ix_chinese_surname_aliases_id"
        ),
        table_name="chinese_surname_aliases",
    )

    op.drop_index(
        op.f(
            "ix_chinese_surname_aliases_"
            "chinese_surname_id"
        ),
        table_name="chinese_surname_aliases",
    )

    op.drop_index(
        op.f(
            "ix_chinese_surname_aliases_"
            "character"
        ),
        table_name="chinese_surname_aliases",
    )

    op.drop_table(
        "chinese_surname_aliases",
    )