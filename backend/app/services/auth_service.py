from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    create_access_token,
)

from app.repositories.user_repository import UserRepository
from app.models.user import User


class AuthService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = UserRepository(db)

    def login(
        self,
        email: str,
        password: str,
    ):
        user = self.repository.get_user_by_email(
            email
        )

        if user is None:
            raise ValueError(
                "Invalid email or password"
            )

        if not verify_password(
            password,
            user.password,
        ):
            raise ValueError(
                "Invalid email or password"
            )

        role_name = (
            user.role_ref.name
            if user.role_ref is not None
            else user.role
        )

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": role_name,
                "role_id": user.role_id,
                "token_version": user.token_version,
            }
        )

        return token


    def get_profile(
        self,
        user_id: int,
    ):
        user = (
            self.repository.db
            .query(User)
            .filter(User.id == user_id)
            .first()
        )

        if user is None:
            return None

        permissions = []

        if user.role_ref:
            permissions = [
                permission.name
                for permission in user.role_ref.permissions
            ]

        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": (
                user.role_ref.name
                if user.role_ref
                else user.role
            ),
            "permissions": permissions,
        }