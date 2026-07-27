from sqlalchemy.orm import Session

from app.models.role import Role


class PermissionService:
    def __init__(self, db: Session):
        self.db = db

    def get_permissions(self, role_id: int) -> list[str]:
        role = (
            self.db.query(Role)
            .filter(Role.id == role_id)
            .first()
        )

        if not role:
            return []

        return [
            permission.name
            for permission in role.permissions
        ]

    def has_permission(
        self,
        role_id: int,
        permission_name: str,
    ) -> bool:
        permissions = self.get_permissions(role_id)

        return permission_name in permissions