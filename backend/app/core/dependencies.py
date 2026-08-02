from fastapi import Depends, HTTPException, status

from app.core.permissions import get_current_user
from app.models.user import User


def require_admin(
    current_user: User = Depends(get_current_user),
):
    """
    Require the authenticated user to have
    the admin RBAC role.
    """

    if (
        current_user.role_ref is None
        or current_user.role_ref.name != "admin"
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user
