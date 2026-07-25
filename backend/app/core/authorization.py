from fastapi import Depends, HTTPException

from app.core.dependencies import get_current_user
from app.core.roles import UserRole


def require_role(*allowed_roles: UserRole):
    def checker(current_user=Depends(get_current_user)):
        if current_user.role not in [
            role.value for role in allowed_roles
        ]:
            raise HTTPException(
                status_code=403,
                detail="Access denied",
            )

        return current_user

    return checker