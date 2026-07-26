from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.base import ApiResponse
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.schemas.pagination import (
    PaginatedResponse,
    PaginationMeta,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=ApiResponse[UserResponse],
)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):

    service = UserService(db)

    result = service.create_user(user)

    return ApiResponse(
        success=True,
        message="User created successfully",
        data=result,
    )


@router.get(
    "/",
    response_model=ApiResponse[PaginatedResponse[UserResponse]],
)
def get_users(
    page: int = Query(
        default=1,
        ge=1,
    ),
    size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    db: Session = Depends(get_db),
):

    service = UserService(db)

    result = service.get_users_paginated(
        page,
        size,
    )

    return ApiResponse(
        success=True,
        message="Users retrieved successfully",
        data=PaginatedResponse(
            items=result["items"],
            meta=PaginationMeta(
                page=result["meta"]["page"],
                size=result["meta"]["size"],
                total=result["meta"]["total"],
            ),
        ),
    )


@router.get(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
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

    return ApiResponse(
        success=True,
        message="User retrieved successfully",
        data=user,
    )


@router.put(
    "/{user_id}",
    response_model=ApiResponse[UserResponse],
)
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db),
):

    service = UserService(db)

    result = service.update_user(
        user_id,
        user,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return ApiResponse(
        success=True,
        message="User updated successfully",
        data=result,
    )


@router.delete(
    "/{user_id}",
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
):

    service = UserService(db)

    deleted = service.delete_user(
        user_id,
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    return ApiResponse(
        success=True,
        message="User deleted successfully",
        data=None,
    )