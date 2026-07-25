from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService

from app.core.dependencies import get_current_user
from app.core.authorization import require_role
from app.core.roles import UserRole
from app.models.user import User


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserResponse,
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    try:
        return service.create_user(user)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[UserResponse],
)
def get_users(
    db: Session = Depends(get_db),
):
    service = UserService(db)

    return service.get_all_users()


# ==========================
# ADMIN ONLY
# ==========================

@router.get(
    "/admin",
    response_model=list[UserResponse],
)
def get_all_users_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role(UserRole.ADMIN),
    ),
):
    service = UserService(db)

    return service.get_all_users()


# ==========================
# JWT Protected Endpoint
# ==========================

@router.get(
    "/me",
    response_model=UserResponse,
)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
def get_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    user = service.get_user_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    updated_user = service.update_user(
        user_id,
        user,
    )

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return updated_user


@router.delete(
    "/{user_id}",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):
    service = UserService(db)

    result = service.delete_user(user_id)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return {
        "success": True,
        "message": "User deleted",
    }