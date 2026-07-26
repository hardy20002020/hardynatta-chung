from fastapi import Depends, HTTPException

from app.core.dependencies import get_current_user
from app.models.user import User


def require_permission(permission_name: str):

    def permission_checker(
        current_user: User = Depends(get_current_user),
    ):

        role = current_user.role_ref

        if role is None:
            raise HTTPException(
                status_code=403,
                detail="No role assigned",
            )

        permissions = {
            permission.name
            for permission in role.permissions
        }

        if permission_name not in permissions:
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

        return current_user

    return permission_checker


def require_admin_create():
    return require_permission(
        "user.create"
    )


def require_user_read():
    return require_permission(
        "user.read"
    )


def require_admin_update():
    return require_permission(
        "user.update"
    )


def require_admin_delete():
    return require_permission(
        "user.delete"
    )