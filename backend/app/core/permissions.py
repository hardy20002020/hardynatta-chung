from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.core.security import decode_access_token
from app.models.user import User


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    payload = decode_access_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

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



def check_admin(user: User):

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



# ==========================
# RBAC Dependencies
# ==========================


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

