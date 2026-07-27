from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)

from app.services.auth_service import AuthService

from app.core.security import (
    decode_access_token,
    security,
)

from app.core.permissions import (
    require_admin_create,
)

from app.core.dependencies import (
    require_permission,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


#
# LOGIN
#

@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):

    service = AuthService(db)

    try:
        token = service.login(
            data.email,
            data.password,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


#
# CURRENT USER
#

@router.get("/me")
def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):

    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        return {
            "success": True,
            "user": payload,
        }

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
        )


#
# ADMIN TEST (ROLE BASED)
#

@router.get("/admin-test")
def admin_test(
    user: dict = Depends(require_admin_create),
):

    return {
        "success": True,
        "message": "Welcome Admin",
        "user": user,
    }


#
# PERMISSION TEST
#

@router.get("/permission-test")
def permission_test(
    user: dict = Depends(
        require_permission(
            "user.read"
        )
    ),
):

    return {
        "success": True,
        "message": "Permission granted",
        "user": user,
    }