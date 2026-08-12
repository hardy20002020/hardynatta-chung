from datetime import date

from app.core.time import utcnow

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Competition(Base):
    __tablename__ = "competitions"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String(200),
        nullable=False,
    )

    code = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    year = Column(
        Integer,
        nullable=False,
    )

    # ======================================================
    # AGE GROUP CLASSIFICATION
    # ======================================================

    age_reference_date = Column(
        Date,
        nullable=True,
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

    groups = relationship(
        "CompetitionGroup",
        back_populates="competition",
        cascade="all, delete-orphan",
    )

    categories = relationship(
        "CompetitionCategory",
        back_populates="competition",
        cascade="all, delete-orphan",
    )

    rounds = relationship(
        "CompetitionRound",
        back_populates="competition",
        cascade="all, delete-orphan",
    )

    registrations = relationship(
        "CompetitionRegistration",
        back_populates="competition",
        cascade="all, delete-orphan",
    )