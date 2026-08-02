from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.core.security import (
    security,
    decode_access_token,
)
from app.db.database import get_db
from app.models.user import User


# ==========================================================
# CURRENT USER / JWT AUTHENTICATION
# ==========================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    try:
        user_id = int(user_id)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    # ======================================================
    # TOKEN VERSION / REVOCATION SECURITY
    # ======================================================

    token_version = payload.get(
        "token_version"
    )

    if token_version is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )

    try:
        token_version = int(token_version)
    except (TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    if token_version != user.token_version:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
        )

    return user


# ==========================================================
# Legacy RBAC (Dipertahankan)
# ==========================================================

def check_admin(user: User):

    # RBAC Baru
    if user.role_ref is not None:
        if user.role_ref.name != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )

        return user

    # RBAC Lama
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return user


def check_user(user: User):

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    return user


# ==========================================================
# Permission Engine
# ==========================================================

def has_permission(
    user: User,
    permission_name: str,
) -> bool:
    """
    Mengecek apakah user memiliki permission tertentu.

    Prioritas:
    1. Role + Permission (RBAC Baru)
    2. Fallback ke role lama
    """

    # RBAC Baru
    if user.role_ref is not None:

        for permission in user.role_ref.permissions:
            if permission.name == permission_name:
                return True

        return False

    # RBAC Lama
    if user.role == "admin":
        return True

    return False


def require_permission(permission_name: str):

    def dependency(
        current_user: User = Depends(get_current_user),
    ):

        if not has_permission(
            current_user,
            permission_name,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Permission "
                    f"'{permission_name}' required"
                ),
            )

        return current_user

    return dependency


# ==========================================================
# Existing Dependencies (Backward Compatibility)
# ==========================================================

def require_admin(
    current_user: User = Depends(get_current_user),
):
    return check_admin(current_user)


def require_admin_create(
    current_user: User = Depends(get_current_user),
):
    return check_admin(current_user)


def require_admin_update(
    current_user: User = Depends(get_current_user),
):
    return check_admin(current_user)


def require_admin_delete(
    current_user: User = Depends(get_current_user),
):
    return check_admin(current_user)


def require_user_read(
    current_user: User = Depends(get_current_user),
):
    return check_user(current_user)