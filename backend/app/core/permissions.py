from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission


def get_current_user(
    token: str,
    db: Session
):

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )

    user_id = payload.get("sub")

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user



def require_permission(permission_name: str):

    def permission_checker(
        current_user: User = Depends(get_current_user),
    ):

        if not current_user.role:
            raise HTTPException(
                status_code=403,
                detail="User has no role",
            )


        permissions = [
            permission.name
            for permission in current_user.role.permissions
        ]


        if permission_name not in permissions:

            raise HTTPException(
                status_code=403,
                detail=f"Missing permission: {permission_name}",
            )


        return current_user


    return permission_checker