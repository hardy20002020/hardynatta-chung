from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role

from app.repositories.user_repository import UserRepository

from app.schemas.user import (
    UserCreate,
    UserUpdate,
)


class UserService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = UserRepository(db)
        self.db = db


    # ==========================================================
    # CREATE
    # ==========================================================

    def create_user(
        self,
        user: UserCreate,
    ) -> User:

        return self.repository.create_user(
            user
        )


    # ==========================================================
    # READ ALL
    # ==========================================================

    def get_all_users(
        self,
    ) -> list[User]:

        return self.repository.get_all_users()


    # ==========================================================
    # PAGINATION
    # ==========================================================

    def get_users_paginated(
        self,
        page: int,
        size: int,
        search: str | None = None,
    ):

        users, total = (
            self.repository.get_users_paginated(
                page=page,
                size=size,
                search=search,
            )
        )

        return {
            "items": users,
            "meta": {
                "page": page,
                "size": size,
                "total": total,
            },
        }


    # ==========================================================
    # READ BY ID
    # ==========================================================

    def get_user_by_id(
        self,
        user_id: int,
    ) -> User | None:

        return self.repository.get_user_by_id(
            user_id
        )


    # ==========================================================
    # READ BY EMAIL
    # ==========================================================

    def get_user_by_email(
        self,
        email: str,
    ) -> User | None:

        return self.repository.get_user_by_email(
            email
        )


    # ==========================================================
    # UPDATE
    # ==========================================================

    def update_user(
        self,
        user_id: int,
        user: UserUpdate,
    ) -> User | None:


        # ======================================================
        # RBAC ROLE VALIDATION
        # ======================================================

        if user.role_id is not None:

            role = (
                self.db.query(Role)
                .filter(
                    Role.id == user.role_id
                )
                .first()
            )

            if role is None:
                raise ValueError(
                    "Role not found"
                )


        return self.repository.update_user(
            user_id,
            user,
        )


    # ==========================================================
    # DELETE
    # ==========================================================

    def delete_user(
        self,
        user_id: int,
    ) -> bool:

        return self.repository.delete_user(
            user_id
        )