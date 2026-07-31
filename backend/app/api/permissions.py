from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
    PermissionResponse,
)

from app.services.permission_service import PermissionService

from app.core.permissions import require_permission


router = APIRouter(
    prefix="/permissions",
    tags=["Permissions"],
)


@router.get(
    "/",
    response_model=list[PermissionResponse],
)
def get_permissions(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("permission.read")
    ),
):
    service = PermissionService(db)

    return service.get_permissions()


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
)
def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("permission.read")
    ),
):
    service = PermissionService(db)

    permission = service.get_permission_by_id(
        permission_id
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    return permission


@router.post(
    "/",
    response_model=PermissionResponse,
)
def create_permission(
    data: PermissionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("permission.create")
    ),
):
    service = PermissionService(db)

    try:
        return service.create_permission(data)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.put(
    "/{permission_id}",
    response_model=PermissionResponse,
)
def update_permission(
    permission_id: int,
    data: PermissionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("permission.update")
    ),
):
    service = PermissionService(db)

    try:
        permission = service.update_permission(
            permission_id,
            data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    return permission


@router.delete(
    "/{permission_id}",
)
def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("permission.delete")
    ),
):
    service = PermissionService(db)

    deleted = service.delete_permission(
        permission_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    return {
        "success": True,
        "message": "Permission deleted successfully",
    }