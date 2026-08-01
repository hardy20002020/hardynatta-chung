from sqlalchemy.orm import Session

from app.models.role import Role
from app.repositories.role_repository import RoleRepository
from app.schemas.role import (
    RoleCreate,
    RoleUpdate,
)


SYSTEM_ROLES = {
    "admin",
    "user",
}


class RoleService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = RoleRepository(db)


    def get_roles(self):
        return self.repository.get_all()


    def get_role_by_id(
        self,
        role_id: int,
    ):
        return self.repository.get_by_id(
            role_id
        )


    def create_role(
        self,
        data: RoleCreate,
    ):
        existing = self.repository.get_by_name(
            data.name
        )

        if existing:
            raise ValueError(
                "Role already exists"
            )

        role = Role(
            name=data.name
        )

        return self.repository.create(
            role
        )


    def update_role(
        self,
        role_id: int,
        data: RoleUpdate,
    ):
        role = self.repository.get_by_id(
            role_id
        )

        if role is None:
            return None

        if role.name.lower() in SYSTEM_ROLES:
            raise ValueError(
                "System role cannot be modified"
            )

        existing = self.repository.get_by_name(
            data.name
        )

        if (
            existing
            and existing.id != role_id
        ):
            raise ValueError(
                "Role already exists"
            )

        return self.repository.update(
            role,
            data.name,
        )


    def delete_role(
        self,
        role_id: int,
    ):
        role = self.repository.get_by_id(
            role_id
        )

        if role is None:
            return False

        if role.name.lower() in SYSTEM_ROLES:
            raise ValueError(
                "System role cannot be deleted"
            )

        return self.repository.delete(
            role
        )