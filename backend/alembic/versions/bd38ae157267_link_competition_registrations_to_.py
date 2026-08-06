"""link competition registrations to categories

Revision ID: bd38ae157267
Revises: b26d8706e325
Create Date: 2026-08-06

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ==========================================================
# ALEMBIC REVISION
# ==========================================================

revision: str = "bd38ae157267"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "b26d8706e325"

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
    Link competition registrations to competition categories.

    A participant may register for multiple categories
    within the same competition.

    The same participant may only register once for the
    same category within the same competition.
    """

    # ======================================================
    # COMPETITION CATEGORY
    # ======================================================

    op.add_column(
        "competition_registrations",
        sa.Column(
            "competition_category_id",
            sa.Integer(),
            nullable=False,
        ),
    )

    # ======================================================
    # REMOVE OLD UNIQUE RULE
    # ======================================================

    op.drop_constraint(
        (
            "uq_competition_registrations_"
            "competition_participant"
        ),
        "competition_registrations",
        type_="unique",
    )

    # ======================================================
    # CATEGORY INDEX
    # ======================================================

    op.create_index(
        (
            "ix_competition_registrations_"
            "competition_category_id"
        ),
        "competition_registrations",
        [
            "competition_category_id",
        ],
        unique=False,
    )

    # ======================================================
    # NEW UNIQUE RULE
    # ======================================================

    op.create_unique_constraint(
        (
            "uq_competition_registrations_"
            "competition_participant_category"
        ),
        "competition_registrations",
        [
            "competition_id",
            "participant_id",
            "competition_category_id",
        ],
    )

    # ======================================================
    # FOREIGN KEY
    # ======================================================

    op.create_foreign_key(
        (
            "fk_competition_registrations_"
            "competition_category_id"
        ),
        "competition_registrations",
        "competition_categories",
        [
            "competition_category_id",
        ],
        [
            "id",
        ],
    )


# ==========================================================
# DOWNGRADE
# ==========================================================

def downgrade() -> None:
    """
    Remove competition category link from registrations.

    Restore the previous rule where a participant may only
    register once within the same competition.
    """

    # ======================================================
    # REMOVE FOREIGN KEY
    # ======================================================

    op.drop_constraint(
        (
            "fk_competition_registrations_"
            "competition_category_id"
        ),
        "competition_registrations",
        type_="foreignkey",
    )

    # ======================================================
    # REMOVE NEW UNIQUE RULE
    # ======================================================

    op.drop_constraint(
        (
            "uq_competition_registrations_"
            "competition_participant_category"
        ),
        "competition_registrations",
        type_="unique",
    )

    # ======================================================
    # REMOVE CATEGORY INDEX
    # ======================================================

    op.drop_index(
        (
            "ix_competition_registrations_"
            "competition_category_id"
        ),
        table_name="competition_registrations",
    )

    # ======================================================
    # RESTORE OLD UNIQUE RULE
    # ======================================================

    op.create_unique_constraint(
        (
            "uq_competition_registrations_"
            "competition_participant"
        ),
        "competition_registrations",
        [
            "competition_id",
            "participant_id",
        ],
    )

    # ======================================================
    # REMOVE CATEGORY COLUMN
    # ======================================================

    op.drop_column(
        "competition_registrations",
        "competition_category_id",
    )