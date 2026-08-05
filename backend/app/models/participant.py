from datetime import date, datetime

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Participant(Base):
    __tablename__ = "participants"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    # ======================================================
    # MAJE MEMBER
    # ======================================================

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    # ======================================================
    # PARTICIPANT PROFILE
    # ======================================================

    chinese_name = Column(
        String(100),
        nullable=True,
    )

    gender = Column(
        String(20),
        nullable=False,
    )

    date_of_birth = Column(
        Date,
        nullable=True,
    )

    # ======================================================
    # CHINESE SURNAME
    # ======================================================

    chinese_surname_id = Column(
        Integer,
        ForeignKey("chinese_surnames.id"),
        nullable=True,
        index=True,
    )

    # ======================================================
    # ETHNICITY
    # ======================================================

    ethnicity_id = Column(
        Integer,
        ForeignKey("ethnicities.id"),
        nullable=True,
        index=True,
    )

    ethnicity_other = Column(
        String(100),
        nullable=True,
    )

    # ======================================================
    # TIMESTAMPS
    # ======================================================

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

    user = relationship(
        "User",
        back_populates="participant",
    )

    chinese_surname = relationship(
        "ChineseSurname",
        back_populates="participants",
    )

    ethnicity = relationship(
        "Ethnicity",
        back_populates="participants",
    )

    registrations = relationship(
        "CompetitionRegistration",
        back_populates="participant",
        cascade="all, delete-orphan",
    )