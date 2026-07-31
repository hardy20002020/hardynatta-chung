from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.permission import Permission


PERMISSIONS = [
    # Users
    "user.create",
    "user.read",
    "user.update",
    "user.delete",

    # Provinces
    "province.create",
    "province.read",
    "province.update",
    "province.delete",

    # Cities
    "city.create",
    "city.read",
    "city.update",
    "city.delete",

    # Dashboard
    "dashboard.read",

    # Roles
    "role.create",
    "role.read",
    "role.update",
    "role.delete",

    # Permissions
    "permission.create",
    "permission.read",
    "permission.update",
    "permission.delete",

    # Role Permissions
    "role.permission.assign",
    "role.permission.revoke",
]


def seed_permissions(db: Session):

    for name in PERMISSIONS:

        existing = (
            db.query(Permission)
            .filter(Permission.name == name)
            .first()
        )

        if existing:
            print(f"✓ {name}")
            continue

        db.add(
            Permission(
                name=name,
            )
        )

        print(f"+ {name}")

    db.commit()


if __name__ == "__main__":

    db = SessionLocal()

    try:
        seed_permissions(db)
        print("\nPermission seed completed.")

    finally:
        db.close()