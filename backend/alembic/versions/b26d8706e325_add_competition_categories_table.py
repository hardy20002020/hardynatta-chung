"""add competition categories table

Revision ID: b26d8706e325
Revises: c4d74d9870e4
Create Date: 2026-08-06 04:43:18.616940

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b26d8706e325"
down_revision: Union[
    str,
    Sequence[str],
    None,
] = "c4d74d9870e4"
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
    """Add competition categories table."""

    op.create_table(
        "competition_categories",
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
                "uq_competition_categories_"
                "competition_id_code"
            ),
        ),
    )

    op.create_index(
        op.f(
            "ix_competition_categories_"
            "competition_id"
        ),
        "competition_categories",
        ["competition_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_competition_categories_id"
        ),
        "competition_categories",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    """Remove competition categories table."""

    op.drop_index(
        op.f(
            "ix_competition_categories_id"
        ),
        table_name="competition_categories",
    )

    op.drop_index(
        op.f(
            "ix_competition_categories_"
            "competition_id"
        ),
        table_name="competition_categories",
    )

    op.drop_table(
        "competition_categories"
    )