"""add competition round judges

Revision ID: 5e1b8b03582b
Revises: 83413bfd2d69
Create Date: 2026-08-06 12:46:45.318968

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "5e1b8b03582b"
down_revision: Union[
    str,
    Sequence[str],
    None,
] = "83413bfd2d69"
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


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        "competition_round_judges",
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
            "user_id",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "judge_order",
            sa.Integer(),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=30),
            server_default="assigned",
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
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint(
            "id"
        ),
        sa.UniqueConstraint(
            "competition_round_id",
            "user_id",
            name=(
                "uq_competition_round_judges_"
                "round_user"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_competition_round_judges_"
            "competition_round_id"
        ),
        "competition_round_judges",
        ["competition_round_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_competition_round_judges_id"
        ),
        "competition_round_judges",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_competition_round_judges_"
            "user_id"
        ),
        "competition_round_judges",
        ["user_id"],
        unique=False,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f(
            "ix_competition_round_judges_"
            "user_id"
        ),
        table_name=(
            "competition_round_judges"
        ),
    )

    op.drop_index(
        op.f(
            "ix_competition_round_judges_id"
        ),
        table_name=(
            "competition_round_judges"
        ),
    )

    op.drop_index(
        op.f(
            "ix_competition_round_judges_"
            "competition_round_id"
        ),
        table_name=(
            "competition_round_judges"
        ),
    )

    op.drop_table(
        "competition_round_judges"
    )