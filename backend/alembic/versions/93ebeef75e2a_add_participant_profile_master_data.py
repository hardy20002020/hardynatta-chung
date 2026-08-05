"""add participant profile master data

Revision ID: 93ebeef75e2a
Revises: 05369c4de1ef
Create Date: 2026-08-05 06:14:33.777027

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# ==========================================================
# ALEMBIC REVISION
# ==========================================================

revision: str = "93ebeef75e2a"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "05369c4de1ef"

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
    Create participant profile master data.

    This migration creates:
    - chinese_surnames
    - ethnicities
    - participants
    """

    # ======================================================
    # CHINESE SURNAMES
    # ======================================================

    op.create_table(
        "chinese_surnames",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "chinese_character",
            sa.String(length=10),
            nullable=False,
        ),

        sa.Column(
            "pinyin",
            sa.String(length=50),
            nullable=False,
        ),

        sa.Column(
            "local_name",
            sa.String(length=100),
            nullable=True,
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

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f(
            "ix_chinese_surnames_"
            "chinese_character"
        ),
        "chinese_surnames",
        ["chinese_character"],
        unique=True,
    )

    op.create_index(
        op.f("ix_chinese_surnames_id"),
        "chinese_surnames",
        ["id"],
        unique=False,
    )

    # ======================================================
    # ETHNICITIES
    # ======================================================

    op.create_table(
        "ethnicities",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "code",
            sa.String(length=30),
            nullable=False,
        ),

        sa.Column(
            "name",
            sa.String(length=100),
            nullable=False,
        ),

        sa.Column(
            "chinese_name",
            sa.String(length=50),
            nullable=True,
        ),

        sa.Column(
            "sort_order",
            sa.Integer(),
            server_default=sa.text("0"),
            nullable=False,
        ),

        sa.Column(
            "is_other",
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

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f("ix_ethnicities_code"),
        "ethnicities",
        ["code"],
        unique=True,
    )

    op.create_index(
        op.f("ix_ethnicities_id"),
        "ethnicities",
        ["id"],
        unique=False,
    )

    # ======================================================
    # PARTICIPANTS
    # ======================================================

    op.create_table(
        "participants",

        sa.Column(
            "id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=False,
        ),

        sa.Column(
            "chinese_name",
            sa.String(length=100),
            nullable=True,
        ),

        sa.Column(
            "gender",
            sa.String(length=20),
            nullable=False,
        ),

        sa.Column(
            "chinese_surname_id",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "ethnicity_id",
            sa.Integer(),
            nullable=True,
        ),

        sa.Column(
            "ethnicity_other",
            sa.String(length=100),
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
            ["chinese_surname_id"],
            ["chinese_surnames.id"],
        ),

        sa.ForeignKeyConstraint(
            ["ethnicity_id"],
            ["ethnicities.id"],
        ),

        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),

        sa.PrimaryKeyConstraint(
            "id",
        ),
    )

    op.create_index(
        op.f(
            "ix_participants_"
            "chinese_surname_id"
        ),
        "participants",
        ["chinese_surname_id"],
        unique=False,
    )

    op.create_index(
        op.f(
            "ix_participants_"
            "ethnicity_id"
        ),
        "participants",
        ["ethnicity_id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_participants_id"),
        "participants",
        ["id"],
        unique=False,
    )

    op.create_index(
        op.f("ix_participants_user_id"),
        "participants",
        ["user_id"],
        unique=True,
    )


# ==========================================================
# DOWNGRADE
# ==========================================================

def downgrade() -> None:
    """
    Remove participant profile master data.
    """

    # ======================================================
    # PARTICIPANTS
    # ======================================================

    op.drop_index(
        op.f("ix_participants_user_id"),
        table_name="participants",
    )

    op.drop_index(
        op.f("ix_participants_id"),
        table_name="participants",
    )

    op.drop_index(
        op.f(
            "ix_participants_"
            "ethnicity_id"
        ),
        table_name="participants",
    )

    op.drop_index(
        op.f(
            "ix_participants_"
            "chinese_surname_id"
        ),
        table_name="participants",
    )

    op.drop_table(
        "participants",
    )

    # ======================================================
    # ETHNICITIES
    # ======================================================

    op.drop_index(
        op.f("ix_ethnicities_id"),
        table_name="ethnicities",
    )

    op.drop_index(
        op.f("ix_ethnicities_code"),
        table_name="ethnicities",
    )

    op.drop_table(
        "ethnicities",
    )

    # ======================================================
    # CHINESE SURNAMES
    # ======================================================

    op.drop_index(
        op.f("ix_chinese_surnames_id"),
        table_name="chinese_surnames",
    )

    op.drop_index(
        op.f(
            "ix_chinese_surnames_"
            "chinese_character"
        ),
        table_name="chinese_surnames",
    )

    op.drop_table(
        "chinese_surnames",
    )