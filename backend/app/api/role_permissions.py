from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.db.database import get_db

from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission

from app.schemas.permission import PermissionResponse

from app.core.permissions import require_permission


router = APIRouter(
    prefix="/role-permissions",
    tags=["Role Permissions"],
)


# ==========================================================
# GET PERMISSIONS BY ROLE
# ==========================================================

@router.get(
    "/{role_id}",
    response_model=list[PermissionResponse],
)
def get_role_permissions(
    role_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("role.read")
    ),
):
    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    return role.permissions


# ==========================================================
# ASSIGN PERMISSION
# ==========================================================

@router.post(
    "/{role_id}/{permission_id}"
)
def assign_permission(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "role.permission.assign"
        )
    ),
):
    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    permission = (
        db.query(Permission)
        .filter(
            Permission.id == permission_id
        )
        .first()
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    existing = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id
            == role_id,
            RolePermission.permission_id
            == permission_id,
        )
        .first()
    )

    if existing:
        return {
            "success": True,
            "message":
                "Permission already assigned",
        }

    role_permission = RolePermission(
        role_id=role_id,
        permission_id=permission_id,
    )

    db.add(role_permission)
    db.commit()

    return {
        "success": True,
        "message": "Permission assigned",
        "role": role.name,
        "permission": permission.name,
    }


# ==========================================================
# REVOKE PERMISSION
# ==========================================================

@router.delete(
    "/{role_id}/{permission_id}"
)
def revoke_permission(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "role.permission.revoke"
        )
    ),
):
    role = (
        db.query(Role)
        .filter(Role.id == role_id)
        .first()
    )

    if role is None:
        raise HTTPException(
            status_code=404,
            detail="Role not found",
        )

    permission = (
        db.query(Permission)
        .filter(
            Permission.id == permission_id
        )
        .first()
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    role_permission = (
        db.query(RolePermission)
        .filter(
            RolePermission.role_id
            == role_id,
            RolePermission.permission_id
            == permission_id,
        )
        .first()
    )

    if role_permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission is not assigned to role",
        )

    db.delete(role_permission)
    db.commit()

    return {
        "success": True,
        "message": "Permission revoked",
        "role": role.name,
        "permission": permission.name,
    }