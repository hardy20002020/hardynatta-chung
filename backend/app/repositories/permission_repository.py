from sqlalchemy.orm import Session

from app.models.permission import Permission


class PermissionRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def get_all(self):
        return (
            self.db
            .query(Permission)
            .all()
        )


    def get_by_id(
        self,
        permission_id: int,
    ):
        return (
            self.db
            .query(Permission)
            .filter(
                Permission.id == permission_id
            )
            .first()
        )


    def get_by_name(
        self,
        name: str,
    ):
        return (
            self.db
            .query(Permission)
            .filter(
                Permission.name == name
            )
            .first()
        )


    def create(
        self,
        permission: Permission,
    ):
        self.db.add(permission)
        self.db.commit()
        self.db.refresh(permission)

        return permission


    def update(
        self,
        permission: Permission,
        name: str,
    ):
        permission.name = name

        self.db.commit()
        self.db.refresh(permission)

        return permission


    def delete(
        self,
        permission: Permission,
    ):
        self.db.delete(permission)
        self.db.commit()

        return True
