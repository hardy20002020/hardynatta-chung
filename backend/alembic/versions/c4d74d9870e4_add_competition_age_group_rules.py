"""add competition age group rules

Revision ID: c4d74d9870e4
Revises: fa767e531dc3
Create Date: 2026-08-05

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ==========================================================
# ALEMBIC REVISION
# ==========================================================

revision: str = "c4d74d9870e4"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "fa767e531dc3"

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
    Add age-group classification rules.

    Competition:
    - age_reference_date

    CompetitionGroup:
    - min_age
    - max_age

    These fields allow MAJE to determine a participant's
    competition group automatically from date of birth.
    """

    # ======================================================
    # COMPETITION AGE REFERENCE DATE
    # ======================================================

    op.add_column(
        "competitions",
        sa.Column(
            "age_reference_date",
            sa.Date(),
            nullable=True,
        ),
    )

    # ======================================================
    # COMPETITION GROUP AGE RANGE
    # ======================================================

    op.add_column(
        "competition_groups",
        sa.Column(
            "min_age",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.add_column(
        "competition_groups",
        sa.Column(
            "max_age",
            sa.Integer(),
            nullable=True,
        ),
    )

    # ======================================================
    # AGE RANGE CONSTRAINTS
    # ======================================================

    op.create_check_constraint(
        "ck_competition_groups_min_age_nonnegative",
        "competition_groups",
        "min_age IS NULL OR min_age >= 0",
    )

    op.create_check_constraint(
        "ck_competition_groups_max_age_nonnegative",
        "competition_groups",
        "max_age IS NULL OR max_age >= 0",
    )

    op.create_check_constraint(
        "ck_competition_groups_age_range",
        "competition_groups",
        (
            "min_age IS NULL "
            "OR max_age IS NULL "
            "OR min_age <= max_age"
        ),
    )


# ==========================================================
# DOWNGRADE
# ==========================================================

def downgrade() -> None:
    """
    Remove age-group classification rules.
    """

    # ======================================================
    # COMPETITION GROUP CONSTRAINTS
    # ======================================================

    op.drop_constraint(
        "ck_competition_groups_age_range",
        "competition_groups",
        type_="check",
    )

    op.drop_constraint(
        "ck_competition_groups_max_age_nonnegative",
        "competition_groups",
        type_="check",
    )

    op.drop_constraint(
        "ck_competition_groups_min_age_nonnegative",
        "competition_groups",
        type_="check",
    )

    # ======================================================
    # COMPETITION GROUP AGE RANGE
    # ======================================================

    op.drop_column(
        "competition_groups",
        "max_age",
    )

    op.drop_column(
        "competition_groups",
        "min_age",
    )

    # ======================================================
    # COMPETITION AGE REFERENCE DATE
    # ======================================================

    op.drop_column(
        "competitions",
        "age_reference_date",
    )