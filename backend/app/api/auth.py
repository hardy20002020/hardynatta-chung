from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
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
from app.core.dependencies import require_admin


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


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
            status_code=401,
            detail=str(e),
        )


@router.get("/me")
def me(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentials.credentials

    payload = decode_access_token(token)

    return {
        "success": True,
        "user": payload,
    }


@router.get("/admin-test")
def admin_test(
    user: dict = Depends(require_admin),
):
    return {
        "success": True,
        "message": "Welcome Admin",
        "user": user,
    }