from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
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

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
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

    registrations = relationship(
        "CompetitionRegistration",
        back_populates="competition",
        cascade="all, delete-orphan",
    )