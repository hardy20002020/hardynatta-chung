from fastapi import Depends, HTTPException

from app.core.dependencies import get_current_user
from app.core.roles import UserRole


def require_role(*allowed_roles: UserRole):
    def checker(
        current_user=Depends(get_current_user),
    ):
        role_name = (
            current_user.role_ref.name
            if current_user.role_ref is not None
            else None
        )

        if role_name not in [
            role.value
            for role in allowed_roles
        ]:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        return current_user

    return checker
