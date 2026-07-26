from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission


def seed():
    db: Session = SessionLocal()

    # Roles
    admin = db.query(Role).filter_by(name="admin").first()
    if not admin:
        admin = Role(name="admin")
        db.add(admin)

    user = db.query(Role).filter_by(name="user").first()
    if not user:
        user = Role(name="user")
        db.add(user)

    db.commit()

    permissions = [
        "user.create",
        "user.read",
        "user.update",
        "user.delete",
    ]

    permission_objects = {}

    for name in permissions:
        permission = (
            db.query(Permission)
            .filter_by(name=name)
            .first()
        )

        if not permission:
            permission = Permission(name=name)
            db.add(permission)
            db.commit()
            db.refresh(permission)

        permission_objects[name] = permission

    db.refresh(admin)
    db.refresh(user)

    mappings = [
        (admin.id, permission_objects["user.create"].id),
        (admin.id, permission_objects["user.read"].id),
        (admin.id, permission_objects["user.update"].id),
        (admin.id, permission_objects["user.delete"].id),
        (user.id, permission_objects["user.read"].id),
    ]

    for role_id, permission_id in mappings:
        exists = (
            db.query(RolePermission)
            .filter_by(
                role_id=role_id,
                permission_id=permission_id,
            )
            .first()
        )

        if not exists:
            db.add(
                RolePermission(
                    role_id=role_id,
                    permission_id=permission_id,
                )
            )

    db.commit()

    print("RBAC seed completed.")


if __name__ == "__main__":
    seed()
