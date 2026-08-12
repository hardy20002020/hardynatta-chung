from app.core.time import utcnow

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class CompetitionRegistration(Base):
    __tablename__ = "competition_registrations"

    __table_args__ = (
        UniqueConstraint(
            "competition_id",
            "participant_id",
            "competition_category_id",
            name=(
                "uq_competition_registrations_"
                "competition_participant_category"
            ),
        ),
        UniqueConstraint(
            "competition_id",
            "registration_number",
            name=(
                "uq_competition_registrations_"
                "competition_registration_number"
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
    # COMPETITION GROUP
    # ======================================================

    competition_group_id = Column(
        Integer,
        ForeignKey("competition_groups.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # COMPETITION CATEGORY
    # ======================================================

    competition_category_id = Column(
        Integer,
        ForeignKey("competition_categories.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # PARTICIPANT
    # ======================================================

    participant_id = Column(
        Integer,
        ForeignKey("participants.id"),
        nullable=False,
        index=True,
    )

    # ======================================================
    # REGISTRATION
    # ======================================================

    registration_number = Column(
        String(50),
        nullable=False,
    )

    status = Column(
        String(30),
        nullable=False,
        default="registered",
        server_default="registered",
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
        back_populates="registrations",
    )

    competition_group = relationship(
        "CompetitionGroup",
        back_populates="registrations",
    )

    competition_category = relationship(
        "CompetitionCategory",
        back_populates="registrations",
    )

    participant = relationship(
        "Participant",
        back_populates="registrations",
    )

    round_entries = relationship(
        "CompetitionRoundEntry",
        back_populates="competition_registration",
        cascade="all, delete-orphan",
    )