from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.repositories.permission_repository import PermissionRepository
from app.schemas.permission import (
    PermissionCreate,
    PermissionUpdate,
)


class PermissionService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = PermissionRepository(db)

    def get_permissions(self):
        return self.repository.get_all()

    def get_permission_by_id(
        self,
        permission_id: int,
    ):
        return self.repository.get_by_id(
            permission_id
        )

    def create_permission(
        self,
        data: PermissionCreate,
    ):
        existing = self.repository.get_by_name(
            data.name
        )

        if existing:
            raise ValueError(
                "Permission already exists"
            )

        permission = Permission(
            name=data.name
        )

        return self.repository.create(
            permission
        )

    def update_permission(
        self,
        permission_id: int,
        data: PermissionUpdate,
    ):
        permission = self.repository.get_by_id(
            permission_id
        )

        if permission is None:
            return None

        existing = self.repository.get_by_name(
            data.name
        )

        if (
            existing is not None
            and existing.id != permission_id
        ):
            raise ValueError(
                "Permission already exists"
            )

        return self.repository.update(
            permission,
            data.name,
        )

    def delete_permission(
        self,
        permission_id: int,
    ):
        permission = self.repository.get_by_id(
            permission_id
        )

        if permission is None:
            return False

        return self.repository.delete(
            permission
        )