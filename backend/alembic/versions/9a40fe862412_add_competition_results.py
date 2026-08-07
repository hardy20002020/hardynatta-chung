"""add competition results

Revision ID: 9a40fe862412
Revises: 1918c4181b77
Create Date: 2026-08-07 06:43:24.286983

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.

revision: str = "9a40fe862412"
down_revision: Union[str, Sequence[str], None] = (
    "1918c4181b77"
)
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create competition results table."""

    op.create_table(
        "competition_results",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "competition_round_entry_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "final_score",
            sa.Numeric(
                precision=10,
                scale=4,
            ),
            nullable=False,
        ),
        sa.Column(
            "rank",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default="finalized",
            nullable=False,
        ),
        sa.Column(
            "finalized_by_user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "finalized_at",
            sa.DateTime(),
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
            ["competition_round_entry_id"],
            ["competition_round_entries.id"],
        ),
        sa.ForeignKeyConstraint(
            ["finalized_by_user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
        sa.UniqueConstraint(
            "competition_round_entry_id",
            name=(
                "uq_competition_results_"
                "round_entry"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_competition_results_"
            "competition_round_entry_id"
        ),
        "competition_results",
        ["competition_round_entry_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_competition_results_"
            "finalized_by_user_id"
        ),
        "competition_results",
        ["finalized_by_user_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_competition_results_id"),
        "competition_results",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop competition results table."""

    op.drop_index(
        op.f("ix_competition_results_id"),
        table_name="competition_results",
    )

    op.drop_index(
        op.f(
            "ix_competition_results_"
            "finalized_by_user_id"
        ),
        table_name="competition_results",
    )

    op.drop_index(
        op.f(
            "ix_competition_results_"
            "competition_round_entry_id"
        ),
        table_name="competition_results",
    )

    op.drop_table(
        "competition_results",
    )
