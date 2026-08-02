from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.security import hash_password

from app.models.user import User

from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


class UserRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    # ==========================================================
    # CREATE USER
    # ==========================================================

    def create_user(
        self,
        user: UserCreate,
    ) -> User:

        existing_user = (
            self.db.query(User)
            .filter(
                User.email == user.email
            )
            .first()
        )

        if existing_user:
            raise ValueError(
                "Email already registered"
            )


        db_user = User(
            name=user.name,
            email=user.email,

            password=hash_password(
                user.password
            ),

            province_id=user.province_id,
            city_id=user.city_id,

            # Default Role = user
            role_id=2,
        )


        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)


        return (
            self.db.query(User)
            .options(
                joinedload(User.province),
                joinedload(User.city),
                joinedload(User.role_ref),
            )
            .filter(
                User.id == db_user.id
            )
            .first()
        )


    # ==========================================================
    # READ ALL USERS
    # ==========================================================

    def get_all_users(
        self,
    ) -> list[User]:

        return (
            self.db.query(User)
            .options(
                joinedload(User.province),
                joinedload(User.city),
                joinedload(User.role_ref),
            )
            .order_by(
                User.id.desc()
            )
            .all()
        )


    # ==========================================================
    # PAGINATION
    # ==========================================================

    def get_users_paginated(
        self,
        page: int,
        size: int,
        search: str | None = None,
    ) -> tuple[list[User], int]:

        offset = (
            page - 1
        ) * size


        query = (
            self.db.query(User)
            .options(
                joinedload(User.province),
                joinedload(User.city),
                joinedload(User.role_ref),
            )
        )


        if search:

            keyword = f"%{search}%"

            query = query.filter(
                or_(
                    User.name.ilike(keyword),
                    User.email.ilike(keyword),
                )
            )


        total = query.count()


        users = (
            query
            .order_by(
                User.id.desc()
            )
            .offset(offset)
            .limit(size)
            .all()
        )


        return users, total


    # ==========================================================
    # READ USER BY ID
    # ==========================================================

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return (
            self.db.query(User)
            .options(
                joinedload(User.province),
                joinedload(User.city),
                joinedload(User.role_ref),
            )
            .filter(
                User.id == user_id
            )
            .first()
        )


    # ==========================================================
    # READ USER BY EMAIL
    # ==========================================================

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .options(
                joinedload(User.role_ref),
                joinedload(User.province),
                joinedload(User.city),
            )
            .filter(
                User.email == email
            )
            .first()
        )


    # ==========================================================
    # UPDATE USER
    # ==========================================================

    def update_user(
        self,
        user_id: int,
        user: UserUpdate,
    ) -> User | None:


        db_user = (
            self.db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )


        if db_user is None:
            return None


        if user.name is not None:
            db_user.name = user.name


        if user.email is not None:
            db_user.email = user.email


        if user.password is not None:
            db_user.password = hash_password(
                user.password
            )


        if user.province_id is not None:
            db_user.province_id = (
                user.province_id
            )


        if user.city_id is not None:
            db_user.city_id = (
                user.city_id
            )


        # ======================================================
        # ACCOUNT STATUS UPDATE
        # ======================================================

        if user.is_active is not None:
            db_user.is_active = (
                user.is_active
            )


        # ======================================================
        # RBAC ROLE UPDATE
        # ======================================================

        if user.role_id is not None:
            db_user.role_id = (
                user.role_id
            )


        self.db.commit()


        # Clear SQLAlchemy cache
        self.db.expire(
            db_user
        )


        # Reload with relationship terbaru
        return (
            self.db.query(User)
            .options(
                joinedload(User.province),
                joinedload(User.city),
                joinedload(User.role_ref),
            )
            .filter(
                User.id == user_id
            )
            .first()
        )


    # ==========================================================
    # DELETE USER
    # ==========================================================

    def delete_user(
        self,
        user_id: int,
    ) -> bool:

        db_user = (
            self.db.query(User)
            .filter(
                User.id == user_id
            )
            .first()
        )


        if db_user is None:
            return False


        self.db.delete(
            db_user
        )

        self.db.commit()


        return True