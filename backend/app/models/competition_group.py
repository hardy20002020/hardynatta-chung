from datetime import datetime

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

    sort_order = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
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

    competition = relationship(
        "Competition",
        back_populates="groups",
    )