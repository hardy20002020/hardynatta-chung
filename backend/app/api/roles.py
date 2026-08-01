from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
    RoleResponse,
)

from app.services.role_service import RoleService

from app.core.permissions import require_permission


router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.get(
    "/",
    response_model=list[RoleResponse],
)
def get_roles(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("role.read")
    ),
):
    service = RoleService(db)

    return service.get_roles()


@router.get(
    "/{role_id}",
    response_model=RoleResponse,
)
def get_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("role.read")
    ),
):
    service = RoleService(db)

    role = service.get_role_by_id(
        role_id
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    return role


@router.post(
    "/",
    response_model=RoleResponse,
)
def create_role(
    data: RoleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("role.create")
    ),
):
    service = RoleService(db)

    try:
        return service.create_role(
            data
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e


@router.put(
    "/{role_id}",
    response_model=RoleResponse,
)
def update_role(
    role_id: int,
    data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("role.update")
    ),
):
    service = RoleService(db)

    try:
        role = service.update_role(
            role_id,
            data,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    return role


@router.delete(
    "/{role_id}",
)
def delete_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("role.delete")
    ),
):
    service = RoleService(db)

    try:
        deleted = service.delete_role(
            role_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        ) from e

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    return {
        "success": True,
        "message": "Role deleted successfully",
    }