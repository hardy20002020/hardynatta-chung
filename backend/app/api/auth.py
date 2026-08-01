from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    CurrentUserResponse,
)

from app.core.security import (
    verify_password,
    create_access_token,
)

from app.core.permissions import (
    get_current_user,
    require_admin,
)

from app.services.audit_log_service import AuditLogService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


audit_service = AuditLogService()


def get_user_permissions(user: User) -> list[str]:
    """
    Mengambil seluruh permission dari role user.

    Prioritas:
    1. RBAC Baru (Role -> Permissions)
    2. Fallback RBAC Lama
    """

    if user.role_ref is not None:
        return sorted(
            [
                permission.name
                for permission in user.role_ref.permissions
            ]
        )

    # Fallback untuk admin lama
    if user.role == "admin":
        return ["*"]

    return []


@router.post(
    "/login",
    response_model=LoginResponse,
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        request.password,
        user.password,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )


    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "role_id": user.role_id,
    }


    access_token = create_access_token(
        data=token_data
    )


    # ======================================================
    # AUDIT LOG - USER LOGIN
    # ======================================================

    audit_service.create_log(
        db,
        user_id=user.id,
        action="LOGIN",
        resource="AUTH",
        description="User login successfully",
    )


    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "role_id": user.role_id,
            "province_id": user.province_id,
            "city_id": user.city_id,
            "permissions": get_user_permissions(user),
        },
    }


@router.get(
    "/me",
    response_model=CurrentUserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):

    return {
        "success": True,
        "message": "Current User",
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "role_id": current_user.role_id,
            "province_id": current_user.province_id,
            "city_id": current_user.city_id,
            "permissions": get_user_permissions(current_user),
        },
    }


@router.get(
    "/admin-test",
    response_model=CurrentUserResponse,
)
def admin_test(
    current_user: User = Depends(require_admin),
):

    return {
        "success": True,
        "message": "Welcome Admin",
        "user": {
            "id": current_user.id,
            "name": current_user.name,
            "email": current_user.email,
            "role": current_user.role,
            "role_id": current_user.role_id,
            "province_id": current_user.province_id,
            "city_id": current_user.city_id,
            "permissions": get_user_permissions(current_user),
        },
    }