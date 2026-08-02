from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer

from app.core.config import settings


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


security = HTTPBearer()


def validate_password_strength(
    password: str,
) -> None:
    """
    Validate password against the MAJE security policy.

    Requirements:
    - Minimum 12 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """

    if len(password) < 12:
        raise ValueError(
            "Password must be at least 12 characters"
        )

    if not any(
        char.isupper()
        for char in password
    ):
        raise ValueError(
            "Password must contain an uppercase letter"
        )

    if not any(
        char.islower()
        for char in password
    ):
        raise ValueError(
            "Password must contain a lowercase letter"
        )

    if not any(
        char.isdigit()
        for char in password
    ):
        raise ValueError(
            "Password must contain a number"
        )

    if not any(
        not char.isalnum()
        for char in password
    ):
        raise ValueError(
            "Password must contain a special character"
        )


def hash_password(password: str) -> str:
    validate_password_strength(password)

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def create_access_token(
    data: dict,
) -> str:
    to_encode = data.copy()

    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update(
        {
            "exp": expire,
        }
    )

    return jwt.encode(
        to_encode,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_access_token(
    token: str,
) -> dict | None:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[
                settings.JWT_ALGORITHM
            ],
        )

    except JWTError:
        return None