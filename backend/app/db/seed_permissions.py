from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.role import Role
from app.models.role_permission import RolePermission


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
]


def seed_permissions(db: Session):

    for permission_name in PERMISSIONS:

        permission = (
            db.query(Permission)
            .filter(
                Permission.name == permission_name
            )
            .first()
        )

        if permission is None:

            db.add(
                Permission(
                    name=permission_name
                )
            )

    db.commit()


def seed_role_permissions(db: Session):

    admin = (
        db.query(Role)
        .filter(Role.name == "admin")
        .first()
    )

    user = (
        db.query(Role)
        .filter(Role.name == "user")
        .first()
    )

    permissions = db.query(Permission).all()

    #
    # ADMIN
    #

    for permission in permissions:

        exists = (
            db.query(RolePermission)
            .filter(
                RolePermission.role_id == admin.id,
                RolePermission.permission_id == permission.id,
            )
            .first()
        )

        if exists is None:

            db.add(
                RolePermission(
                    role_id=admin.id,
                    permission_id=permission.id,
                )
            )

    #
    # USER
    #

    user_permissions = [
        "dashboard.read",
        "user.read",
    ]

    for permission_name in user_permissions:

        permission = (
            db.query(Permission)
            .filter(
                Permission.name == permission_name
            )
            .first()
        )

        exists = (
            db.query(RolePermission)
            .filter(
                RolePermission.role_id == user.id,
                RolePermission.permission_id == permission.id,
            )
            .first()
        )

        if exists is None:

            db.add(
                RolePermission(
                    role_id=user.id,
                    permission_id=permission.id,
                )
            )

    db.commit()