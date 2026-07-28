from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
)

from app.core.security import (
    verify_password,
    create_access_token,
)

from app.core.permissions import (
    get_current_user,
    require_admin,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )


    if not verify_password(
        request.password,
        user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
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
        }
    }



@router.get(
    "/me"
)
def get_me(
    current_user: User = Depends(get_current_user)
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
        }
    }



@router.get(
    "/admin-test"
)
def admin_test(
    current_user: User = Depends(require_admin)
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
        }
    }