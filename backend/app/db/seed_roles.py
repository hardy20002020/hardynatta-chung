from sqlalchemy.orm import Session

from app.models.role import Role


ROLES = [
    "admin",
    "manager",
    "user",
]


def seed_roles(db: Session) -> None:
    """
    Seed the default MAJE RBAC roles.

    The operation is idempotent and can safely
    be executed multiple times.
    """

    for role_name in ROLES:
        exists = (
            db.query(Role)
            .filter(Role.name == role_name)
            .first()
        )

        if exists is None:
            db.add(
                Role(
                    name=role_name,
                )
            )

    db.commit()