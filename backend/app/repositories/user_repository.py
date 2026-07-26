from sqlalchemy import func, or_
from sqlalchemy.orm import Session, joinedload

from app.core.security import hash_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserRepository:

    def __init__(self, db: Session):
        self.db = db


    def create_user(
        self,
        user: UserCreate,
    ) -> User:

        existing_user = (
            self.db.query(User)
            .filter(User.email == user.email)
            .first()
        )

        if existing_user:
            raise ValueError(
                "Email already registered"
            )

        db_user = User(
            name=user.name,
            email=user.email,
            password=hash_password(user.password),
            province_id=user.province_id,
            city_id=user.city_id,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user


    def get_all_users(
        self,
    ) -> list[User]:

        return (
            self.db.query(User)
            .options(
                joinedload(User.province),
                joinedload(User.city),
            )
            .all()
        )


    def get_users_paginated(
        self,
        page: int,
        size: int,
        search: str | None = None,
    ) -> tuple[list[User], int]:

        offset = (page - 1) * size

        query = (
            self.db.query(User)
            .options(
                joinedload(User.province),
                joinedload(User.city),
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
            .offset(offset)
            .limit(size)
            .all()
        )

        return users, total


    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return (
            self.db.query(User)
            .options(
                joinedload(User.province),
                joinedload(User.city),
            )
            .filter(User.id == user_id)
            .first()
        )


    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:

        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )


    def update_user(
        self,
        user_id: int,
        user: UserUpdate,
    ) -> User | None:

        db_user = (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if db_user is None:
            return None


        db_user.name = user.name
        db_user.email = user.email
        db_user.province_id = user.province_id
        db_user.city_id = user.city_id


        self.db.commit()
        self.db.refresh(db_user)

        return db_user


    def delete_user(
        self,
        user_id: int,
    ) -> bool:

        db_user = (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if db_user is None:
            return False


        self.db.delete(db_user)
        self.db.commit()

        return True