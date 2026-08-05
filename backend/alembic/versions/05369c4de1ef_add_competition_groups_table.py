"""add competition groups table

Revision ID: 05369c4de1ef
Revises: cc0a17b64f6a
Create Date: 2026-08-05 05:10:50.055982

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ==========================================================
# ALEMBIC REVISION
# ==========================================================

revision: str = "05369c4de1ef"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "cc0a17b64f6a"

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
    Create the competition_groups table.

    Competition groups belong to a competition
    and represent organizer-defined participant
    categories.
    """

    op.create_table(
        "competition_groups",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "competition_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "code",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "sort_order",
            sa.Integer(),
            server_default=sa.text("0"),
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
            ["competition_id"],
            ["competitions.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id",
        ),

        sa.UniqueConstraint(
            "competition_id",
            "code",
            name=(
                "uq_competition_groups_"
                "competition_id_code"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_competition_groups_"
            "competition_id"
        ),
        "competition_groups",
        ["competition_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_competition_groups_id"),
        "competition_groups",
        ["id"],
        unique=False,
    )


# ==========================================================
# DOWNGRADE
# ==========================================================

def downgrade() -> None:
    """
    Remove the competition_groups table.
    """

    op.drop_index(
        op.f("ix_competition_groups_id"),
        table_name="competition_groups",
    )

    op.drop_index(
        op.f(
            "ix_competition_groups_"
            "competition_id"
        ),
        table_name="competition_groups",
    )

    op.drop_table(
        "competition_groups",
    )