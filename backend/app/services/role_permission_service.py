from sqlalchemy.orm import Session

from app.repositories.role_permission_repository import (
    RolePermissionRepository,
)


class RolePermissionService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = RolePermissionRepository(db)


    def get_permissions(
        self,
        role_id: int,
    ):
        return self.repository.get_permissions_by_role(
            role_id
        )


    def assign(
        self,
        role_id: int,
        permission_id: int,
    ):
        role = self.repository.get_role(role_id)

        if role is None:
            raise ValueError(
                "Role not found"
            )

        permission = self.repository.get_permission(
            permission_id
        )

        if permission is None:
            raise ValueError(
                "Permission not found"
            )

        return self.repository.assign(
            role_id,
            permission_id,
        )


    def remove(
        self,
        role_id: int,
        permission_id: int,
    ):
        return self.repository.remove(
            role_id,
            permission_id,
        )
