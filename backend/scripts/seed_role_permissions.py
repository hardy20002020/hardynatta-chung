from app.db.database import SessionLocal
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import RolePermission

db = SessionLocal()

try:
    admin = db.query(Role).filter(Role.name == "admin").first()

    if not admin:
        raise Exception("Admin role not found")

    permissions = db.query(Permission).all()

    for permission in permissions:

        exists = (
            db.query(RolePermission)
            .filter(
                RolePermission.role_id == admin.id,
                RolePermission.permission_id == permission.id,
            )
            .first()
        )

        if exists:
            print(f"✓ {permission.name}")
            continue

        db.add(
            RolePermission(
                role_id=admin.id,
                permission_id=permission.id,
            )
        )

        print(f"+ {permission.name}")

    db.commit()

    print("\nAdmin role permissions seeded successfully.")

finally:
    db.close()