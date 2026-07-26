from sqlalchemy.orm import Session

from app.core.security import (
    verify_password,
    create_access_token,
)

from app.repositories.user_repository import UserRepository


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

        # Ambil role dari tabel roles jika tersedia
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
            }
        )

        return token