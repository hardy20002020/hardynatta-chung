from sqlalchemy.orm import Session

from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission


class RolePermissionRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def get_role(
        self,
        role_id: int,
    ):
        return (
            self.db
            .query(Role)
            .filter(Role.id == role_id)
            .first()
        )


    def get_permission(
        self,
        permission_id: int,
    ):
        return (
            self.db
            .query(Permission)
            .filter(Permission.id == permission_id)
            .first()
        )


    def get_permissions_by_role(
        self,
        role_id: int,
    ):
        role = self.get_role(role_id)

        if role is None:
            return None

        return role.permissions


    def assign(
        self,
        role_id: int,
        permission_id: int,
    ):
        existing = (
            self.db
            .query(RolePermission)
            .filter(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
            .first()
        )

        if existing:
            return existing

        item = RolePermission(
            role_id=role_id,
            permission_id=permission_id,
        )

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item


    def remove(
        self,
        role_id: int,
        permission_id: int,
    ):

        item = (
            self.db
            .query(RolePermission)
            .filter(
                RolePermission.role_id == role_id,
                RolePermission.permission_id == permission_id,
            )
            .first()
        )

        if item is None:
            return False

        self.db.delete(item)
        self.db.commit()

        return True
