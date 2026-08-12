from app.core.time import utcnow

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class ChineseSurnameAlias(Base):
    __tablename__ = "chinese_surname_aliases"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    chinese_surname_id = Column(
        Integer,
        ForeignKey("chinese_surnames.id"),
        nullable=False,
        index=True,
    )

    character = Column(
        String(10),
        nullable=False,
        unique=True,
        index=True,
    )

    variant_type = Column(
        String(30),
        nullable=False,
    )

    is_primary = Column(
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

    chinese_surname = relationship(
        "ChineseSurname",
        back_populates="aliases",
    )