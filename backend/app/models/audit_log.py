from app.core.time import utcnow

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
    )

    action = Column(
        String(50),
        nullable=False,
    )

    resource = Column(
        String(100),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=utcnow,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="audit_logs",
    )