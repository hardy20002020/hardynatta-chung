from datetime import datetime, timedelta, UTC
import secrets

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.user_session import UserSession

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    CurrentUserResponse,
    ChangePasswordRequest,
    RefreshTokenRequest,
    RefreshTokenResponse,
)

from app.core.security import (
    verify_password,
    hash_password,
    create_access_token,
    create_refresh_token,
    hash_refresh_token,
    get_refresh_token_expiry,
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
    Return all permissions assigned through
    the user's RBAC role.
    """

    if user.role_ref is None:
        return []

    return sorted(
        [
            permission.name
            for permission in user.role_ref.permissions
        ]
    )


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
    # REFRESH TOKEN / SESSION
    # ======================================================

    refresh_token = create_refresh_token()

    # Every login starts a new refresh-token family.
    # All rotations originating from this login
    # retain the same family identifier.
    token_family = secrets.token_hex(32)

    user_agent = request.headers.get(
        "user-agent"
    )

    if user_agent is not None:
        user_agent = user_agent[:512]

    client_ip = None

    if request.client is not None:
        client_ip = request.client.host

        if client_ip is not None:
            client_ip = client_ip[:45]

    session = UserSession(
        user_id=user.id,
        refresh_token_hash=hash_refresh_token(
            refresh_token
        ),
        expires_at=get_refresh_token_expiry(),
        created_at=now,
        token_family=token_family,
        user_agent=user_agent,
        ip_address=client_ip,
    )

    db.add(session)
    db.commit()


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
        "refresh_token": refresh_token,
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
# REFRESH TOKEN ROTATION
# ==========================================================

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    """
    Rotate a valid refresh token and issue
    a new access token and refresh token.
    """

    now = datetime.now(UTC).replace(
        tzinfo=None
    )

    token_hash = hash_refresh_token(
        refresh_data.refresh_token
    )

    session = (
        db.query(UserSession)
        .filter(
            UserSession.refresh_token_hash
            == token_hash
        )
        .first()
    )

    if session is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if session.revoked_at is not None:

        # A refresh token that was already rotated and is
        # presented again indicates possible token replay.
        # Revoke the complete token family so any descendant
        # refresh token can no longer be used.
        if session.revoke_reason == "rotated":
            (
                db.query(UserSession)
                .filter(
                    UserSession.token_family
                    == session.token_family,
                )
                .update(
                    {
                        UserSession.revoked_at: now,
                        UserSession.revoke_reason:
                            "reuse_detected",
                    },
                    synchronize_session=False,
                )
            )

            db.commit()

            audit_service.create_log(
                db,
                user_id=session.user_id,
                action="REFRESH_TOKEN_REUSE",
                resource="AUTH",
                description=(
                    "Refresh token reuse detected; "
                    "token family revoked"
                ),
            )

            raise HTTPException(
                status_code=401,
                detail=(
                    "Refresh token reuse detected; "
                    "session revoked"
                ),
            )

        raise HTTPException(
            status_code=401,
            detail="Refresh token has been revoked",
        )

    if session.expires_at <= now:
        session.revoked_at = now
        session.revoke_reason = "expired"
        db.commit()

        raise HTTPException(
            status_code=401,
            detail="Refresh token has expired",
        )

    user = (
        db.query(User)
        .filter(
            User.id == session.user_id
        )
        .first()
    )

    if user is None:
        session.revoked_at = now
        db.commit()

        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token",
        )

    if not user.is_active:
        session.revoked_at = now
        db.commit()

        raise HTTPException(
            status_code=403,
            detail="Account is inactive",
        )


    # ======================================================
    # ROTATE CURRENT SESSION
    # ======================================================

    new_refresh_token = create_refresh_token()

    session.last_used_at = now
    session.revoked_at = now
    session.revoke_reason = "rotated"

    new_session = UserSession(
        user_id=user.id,
        refresh_token_hash=hash_refresh_token(
            new_refresh_token
        ),
        expires_at=get_refresh_token_expiry(),
        created_at=now,
        token_family=session.token_family,
        user_agent=session.user_agent,
        ip_address=session.ip_address,
    )

    db.add(new_session)


    # ======================================================
    # CREATE NEW ACCESS TOKEN
    # ======================================================

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

    db.commit()


    audit_service.create_log(
        db,
        user_id=user.id,
        action="TOKEN_REFRESH",
        resource="AUTH",
        description="Refresh token rotated successfully",
    )


    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer",
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

    now = datetime.now(UTC).replace(
        tzinfo=None
    )

    (
        db.query(UserSession)
        .filter(
            UserSession.user_id == current_user.id,
            UserSession.revoked_at.is_(None),
        )
        .update(
            {
                UserSession.revoked_at: now,
                UserSession.revoke_reason: "logout",
            },
            synchronize_session=False,
        )
    )

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

    now = datetime.now(UTC).replace(
        tzinfo=None
    )

    (
        db.query(UserSession)
        .filter(
            UserSession.user_id == current_user.id,
            UserSession.revoked_at.is_(None),
        )
        .update(
            {
                UserSession.revoked_at: now,
                UserSession.revoke_reason: "password_change",
            },
            synchronize_session=False,
        )
    )

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
