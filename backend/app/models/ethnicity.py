from app.core.time import utcnow

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class Ethnicity(Base):
    __tablename__ = "ethnicities"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    code = Column(
        String(30),
        nullable=False,
        unique=True,
        index=True,
    )

    name = Column(
        String(100),
        nullable=False,
    )

    chinese_name = Column(
        String(50),
        nullable=True,
    )

    sort_order = Column(
        Integer,
        nullable=False,
        default=0,
        server_default="0",
    )

    is_other = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default="false",
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

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

    participants = relationship(
        "Participant",
        back_populates="ethnicity",
    )