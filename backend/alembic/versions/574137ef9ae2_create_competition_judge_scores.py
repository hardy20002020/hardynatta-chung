"""create competition judge scores

Revision ID: 574137ef9ae2
Revises: 5e1b8b03582b
Create Date: 2026-08-06 13:28:54.220758

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "574137ef9ae2"
down_revision: Union[str, Sequence[str], None] = "5e1b8b03582b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create competition judge scores table."""

    op.create_table(
        "competition_judge_scores",
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
            "competition_round_judge_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "total_score",
            sa.Numeric(
                precision=10,
                scale=4,
            ),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default="draft",
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "submitted_at",
            sa.DateTime(),
            nullable=True,
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
            ["competition_round_judge_id"],
            ["competition_round_judges.id"],
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
        sa.UniqueConstraint(
            "competition_round_entry_id",
            "competition_round_judge_id",
            name="uq_competition_judge_scores_entry_judge",
        ),
    )

    op.create_index(
        op.f(
            "ix_competition_judge_scores_"
            "competition_round_entry_id"
        ),
        "competition_judge_scores",
        ["competition_round_entry_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_competition_judge_scores_"
            "competition_round_judge_id"
        ),
        "competition_judge_scores",
        ["competition_round_judge_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_competition_judge_scores_id"),
        "competition_judge_scores",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop competition judge scores table."""

    op.drop_index(
        op.f("ix_competition_judge_scores_id"),
        table_name="competition_judge_scores",
    )

    op.drop_index(
        op.f(
            "ix_competition_judge_scores_"
            "competition_round_judge_id"
        ),
        table_name="competition_judge_scores",
    )

    op.drop_index(
        op.f(
            "ix_competition_judge_scores_"
            "competition_round_entry_id"
        ),
        table_name="competition_judge_scores",
    )

    op.drop_table(
        "competition_judge_scores",
    )