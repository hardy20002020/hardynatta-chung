"""add scoring criteria and judge score details

Revision ID: 1918c4181b77
Revises: 574137ef9ae2
Create Date: 2026-08-06 13:43:49.261498

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1918c4181b77"
down_revision: Union[str, Sequence[str], None] = "574137ef9ae2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create scoring criteria and judge score detail tables."""

    # ======================================================
    # COMPETITION SCORING CRITERIA
    # ======================================================

    op.create_table(
        "competition_scoring_criteria",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "competition_round_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "code",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=150),
            nullable=False,
        ),
        sa.Column(
            "description",
            sa.String(length=500),
            nullable=True,
        ),
        sa.Column(
            "weight",
            sa.Numeric(
                precision=7,
                scale=4,
            ),
            nullable=False,
        ),
        sa.Column(
            "min_score",
            sa.Numeric(
                precision=10,
                scale=4,
            ),
            server_default="0",
            nullable=False,
        ),
        sa.Column(
            "max_score",
            sa.Numeric(
                precision=10,
                scale=4,
            ),
            server_default="100",
            nullable=False,
        ),
        sa.Column(
            "sort_order",
            sa.Integer(),
            server_default="0",
            nullable=False,
        ),
        sa.Column(
            "is_active",
            sa.Boolean(),
            server_default="true",
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
            ["competition_round_id"],
            ["competition_rounds.id"],
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
        sa.UniqueConstraint(
            "competition_round_id",
            "code",
            name=(
                "uq_competition_scoring_criteria_"
                "round_code"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_competition_scoring_criteria_"
            "competition_round_id"
        ),
        "competition_scoring_criteria",
        ["competition_round_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_competition_scoring_criteria_id"),
        "competition_scoring_criteria",
        ["id"],
        unique=False,
    )

    # ======================================================
    # COMPETITION JUDGE SCORE DETAILS
    # ======================================================

    op.create_table(
        "competition_judge_score_details",
        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "competition_judge_score_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "competition_scoring_criterion_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "score",
            sa.Numeric(
                precision=10,
                scale=4,
            ),
            nullable=False,
        ),
        sa.Column(
            "weighted_score",
            sa.Numeric(
                precision=10,
                scale=4,
            ),
            nullable=True,
        ),
        sa.Column(
            "source",
            sa.String(length=30),
            server_default="human",
            nullable=False,
        ),
        sa.Column(
            "notes",
            sa.Text(),
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
            ["competition_judge_score_id"],
            ["competition_judge_scores.id"],
        ),
        sa.ForeignKeyConstraint(
            ["competition_scoring_criterion_id"],
            ["competition_scoring_criteria.id"],
        ),
        sa.PrimaryKeyConstraint(
            "id",
        ),
        sa.UniqueConstraint(
            "competition_judge_score_id",
            "competition_scoring_criterion_id",
            name=(
                "uq_competition_judge_score_details_"
                "score_criterion"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_competition_judge_score_details_"
            "competition_judge_score_id"
        ),
        "competition_judge_score_details",
        ["competition_judge_score_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_competition_judge_score_details_"
            "competition_scoring_criterion_id"
        ),
        "competition_judge_score_details",
        ["competition_scoring_criterion_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_competition_judge_score_details_id"),
        "competition_judge_score_details",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Drop judge score detail and scoring criteria tables."""

    # ======================================================
    # COMPETITION JUDGE SCORE DETAILS
    # ======================================================

    op.drop_index(
        op.f("ix_competition_judge_score_details_id"),
        table_name="competition_judge_score_details",
    )

    op.drop_index(
        op.f(
            "ix_competition_judge_score_details_"
            "competition_scoring_criterion_id"
        ),
        table_name="competition_judge_score_details",
    )

    op.drop_index(
        op.f(
            "ix_competition_judge_score_details_"
            "competition_judge_score_id"
        ),
        table_name="competition_judge_score_details",
    )

    op.drop_table(
        "competition_judge_score_details",
    )

    # ======================================================
    # COMPETITION SCORING CRITERIA
    # ======================================================

    op.drop_index(
        op.f("ix_competition_scoring_criteria_id"),
        table_name="competition_scoring_criteria",
    )

    op.drop_index(
        op.f(
            "ix_competition_scoring_criteria_"
            "competition_round_id"
        ),
        table_name="competition_scoring_criteria",
    )

    op.drop_table(
        "competition_scoring_criteria",
    )