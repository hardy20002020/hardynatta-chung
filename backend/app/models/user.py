from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.base import Base


class User(Base):

    __tablename__ = "users"


    # ==========================================================
    # BASIC
    # ==========================================================

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


    # ==========================================================
    # RBAC ROLE
    # ==========================================================

    role_id = Column(
        Integer,
        ForeignKey("roles.id"),
        nullable=False,
        default=2,
    )


    # ==========================================================
    # LOCATION
    # ==========================================================

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


    # ==========================================================
    # RELATIONSHIPS
    # ==========================================================

    role_ref = relationship(
        "Role",
        back_populates="users",
    )


    province = relationship(
        "Province",
        back_populates="users",
    )


    city = relationship(
        "City",
        back_populates="users",
    )


    # ==========================================================
    # COMPATIBILITY FOR RESPONSE SCHEMA
    # ==========================================================

    @property
    def role(self):
        """
        Return role name from RBAC relation.
        Used by UserResponse schema.
        """

        if self.role_ref:
            return self.role_ref.name

        return None