from datetime import datetime, timedelta, UTC

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    CurrentUserResponse,
    ChangePasswordRequest,
)

from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
)

from app.core.permissions import (
    get_current_user,
    require_admin,
)

from app.core.config import settings
from app.core.rate_limit import limiter

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


# ==========================================================
# LOGIN
# ==========================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
@limiter.limit(settings.LOGIN_RATE_LIMIT)
def login(
    request: Request,
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):

    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    # ======================================================
    # ACCOUNT STATUS / LOCKOUT SECURITY
    # ======================================================

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="Account is inactive",
        )


    now = datetime.now(UTC).replace(tzinfo=None)


    # Existing lockout still active
    if (
        user.locked_until is not None
        and user.locked_until > now
    ):
        raise HTTPException(
            status_code=423,
            detail="Account is temporarily locked",
        )


    # Expired lockout: reset state
    if (
        user.locked_until is not None
        and user.locked_until <= now
    ):
        user.failed_login_attempts = 0
        user.locked_until = None
        db.commit()


    # Password validation
    if not verify_password(
        login_data.password,
        user.password,
    ):
        user.failed_login_attempts += 1

        if (
            user.failed_login_attempts
            >= settings.MAX_FAILED_LOGIN_ATTEMPTS
        ):
            user.locked_until = (
                now
                + timedelta(
                    minutes=(
                        settings.ACCOUNT_LOCKOUT_MINUTES
                    )
                )
            )

        db.commit()

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )


    # Successful login resets failed attempts
    if (
        user.failed_login_attempts != 0
        or user.locked_until is not None
    ):
        user.failed_login_attempts = 0
        user.locked_until = None
        db.commit()


    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
        "role_id": user.role_id,
        "token_version": user.token_version,
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
            "is_active": user.is_active,
            "permissions": get_user_permissions(user),
        },
    }


# ==========================================================
# LOGOUT / TOKEN REVOCATION
# ==========================================================

@router.post(
    "/logout",
)
def logout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Revoke all access tokens issued with the
    current token version.
    """

    current_user.token_version += 1

    db.commit()
    db.refresh(current_user)

    # ======================================================
    # AUDIT LOG - USER LOGOUT
    # ======================================================

    audit_service.create_log(
        db,
        user_id=current_user.id,
        action="LOGOUT",
        resource="AUTH",
        description="User logout successfully",
    )

    return {
        "success": True,
        "message": "Logout successful",
    }


# ==========================================================
# CHANGE PASSWORD
# ==========================================================

@router.post(
    "/change-password",
)
def change_password(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Change the authenticated user's password
    and revoke all previously issued tokens.
    """

    if not verify_password(
        password_data.current_password,
        current_user.password,
    ):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect",
        )

    if verify_password(
        password_data.new_password,
        current_user.password,
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "New password must be different "
                "from current password"
            ),
        )

    try:
        new_password_hash = hash_password(
            password_data.new_password
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    current_user.password = new_password_hash

    # Revoke every token issued before
    # this password change.
    current_user.token_version += 1

    db.commit()
    db.refresh(current_user)

    audit_service.create_log(
        db,
        user_id=current_user.id,
        action="PASSWORD_CHANGE",
        resource="AUTH",
        description="User password changed successfully",
    )

    return {
        "success": True,
        "message": "Password changed successfully",
    }


# ==========================================================
# CURRENT USER
# ==========================================================

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
            "is_active": current_user.is_active,
            "permissions": get_user_permissions(current_user),
        },
    }


# ==========================================================
# ADMIN TEST
# ==========================================================

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
            "is_active": current_user.is_active,
            "permissions": get_user_permissions(current_user),
        },
    }
