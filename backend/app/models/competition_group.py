from app.core.time import utcnow

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class CompetitionGroup(Base):
    __tablename__ = "competition_groups"

    __table_args__ = (
        UniqueConstraint(
            "competition_id",
            "code",
            name=(
                "uq_competition_groups_"
                "competition_id_code"
            ),
        ),
        CheckConstraint(
            (
                "min_age IS NULL "
                "OR min_age >= 0"
            ),
            name=(
                "ck_competition_groups_"
                "min_age_nonnegative"
            ),
        ),
        CheckConstraint(
            (
                "max_age IS NULL "
                "OR max_age >= 0"
            ),
            name=(
                "ck_competition_groups_"
                "max_age_nonnegative"
            ),
        ),
        CheckConstraint(
            (
                "min_age IS NULL "
                "OR max_age IS NULL "
                "OR min_age <= max_age"
            ),
            name=(
                "ck_competition_groups_"
                "age_range"
            ),
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    competition_id = Column(
        Integer,
        ForeignKey("competitions.id"),
        nullable=False,
        index=True,
    )

    code = Column(
        String(20),
        nullable=False,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    # ======================================================
    # AGE GROUP RULES
    # ======================================================

    min_age = Column(
        Integer,
        nullable=True,
    )

    max_age = Column(
        Integer,
        nullable=True,
    )

    # ======================================================
    # DISPLAY ORDER
    # ======================================================

    sort_order = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    # ======================================================
    # STATUS
    # ======================================================

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    # ======================================================
    # TIMESTAMPS
    # ======================================================

    created_at = Column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=utcnow,
        onupdate=utcnow,
        nullable=False,
    )

    # ======================================================
    # RELATIONSHIPS
    # ======================================================

    competition = relationship(
        "Competition",
        back_populates="groups",
    )

    registrations = relationship(
        "CompetitionRegistration",
        back_populates="competition_group",
    )