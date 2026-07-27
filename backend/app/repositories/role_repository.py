from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db


    def get_all(self):
        return (
            self.db
            .query(Role)
            .all()
        )


    def get_by_id(
        self,
        role_id: int,
    ):
        return (
            self.db
            .query(Role)
            .filter(
                Role.id == role_id
            )
            .first()
        )


    def get_by_name(
        self,
        name: str,
    ):
        return (
            self.db
            .query(Role)
            .filter(
                Role.name == name
            )
            .first()
        )


    def create(
        self,
        role: Role,
    ):
        self.db.add(role)
        self.db.commit()
        self.db.refresh(role)

        return role


    def update(
        self,
        role: Role,
        name: str,
    ):
        role.name = name

        self.db.commit()
        self.db.refresh(role)

        return role


    def delete(
        self,
        role: Role,
    ):
        self.db.delete(role)
        self.db.commit()

        return True
