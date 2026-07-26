from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    email = Column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    password = Column(
        String,
        nullable=False,
    )

    # RBAC lama (sementara dipertahankan)
    role = Column(
        String,
        nullable=False,
        default="user",
    )

    # RBAC baru
    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=True,
    )

    province_id = Column(
        Integer,
        ForeignKey("provinces.id"),
        nullable=True,
    )

    city_id = Column(
        Integer,
        ForeignKey("cities.id"),
        nullable=True,
    )

    province = relationship(
        "Province",
        back_populates="users",
    )

    city = relationship(
        "City",
        back_populates="users",
    )

    # Relationship ke tabel roles
    role_ref = relationship(
        "Role",
        back_populates="users",
    )