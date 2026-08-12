from app.core.time import utcnow

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class CompetitionCategory(Base):
    __tablename__ = "competition_categories"

    __table_args__ = (
        UniqueConstraint(
            "competition_id",
            "code",
            name=(
                "uq_competition_categories_"
                "competition_id_code"
            ),
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ======================================================
    # COMPETITION
    # ======================================================

    competition_id = Column(
        Integer,
        ForeignKey("competitions.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # CATEGORY
    # ======================================================

    code = Column(
        String(50),
        nullable=False,
    )

    name = Column(
        String(150),
        nullable=False,
    )

    description = Column(
        String(500),
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
        back_populates="categories",
    )

    registrations = relationship(
        "CompetitionRegistration",
        back_populates="competition_category",
    )
