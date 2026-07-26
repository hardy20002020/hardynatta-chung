from fastapi import Depends, HTTPException, status

from app.core.dependencies import get_current_user
from app.models.user import User


def require_admin(
    current_user: User = Depends(get_current_user),
):
    """
    Allow access only for admin users.
    """

    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user


def require_user(
    current_user: User = Depends(get_current_user),
):
    """
    Allow authenticated users.
    """

    return current_user


def require_roles(*roles: str):
    """
    Dynamic role checker.

    Example:
        Depends(require_roles("admin", "manager"))
    """

    def role_checker(
        current_user: User = Depends(get_current_user),
    ):

        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )

        return current_user

    return role_checker