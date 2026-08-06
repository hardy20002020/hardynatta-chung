from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.role import Role


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

    # Competitions
    "competition.create",
    "competition.read",
    "competition.update",
    "competition.delete",

    # Competition Groups
    "competition_group.create",
    "competition_group.read",
    "competition_group.update",
    "competition_group.delete",

    # Competition Registrations
    "competition_registration.create",
    "competition_registration.read",
    "competition_registration.update",
    "competition_registration.delete",

    # Participants - Administration
    "participant.create",
    "participant.read",
    "participant.update",
    "participant.delete",

    # Participants - Self Service Portal
    "participant.self.create",
    "participant.self.read",
    "participant.self.update",
]


ROLE_PERMISSIONS = {
    "admin": PERMISSIONS,

    "manager": [
        "dashboard.read",
        "competition.read",
        "competition_group.read",
        "competition_registration.read",
        "participant.read",
    ],

    "user": [
        "user.read",
        "participant.self.create",
        "participant.self.read",
        "participant.self.update",
    ],
}


def seed_permissions(
    db: Session,
) -> None:
    """
    Seed all MAJE permissions.

    This operation is idempotent.
    """

    for permission_name in PERMISSIONS:
        permission = (
            db.query(Permission)
            .filter(
                Permission.name
                == permission_name
            )
            .first()
        )

        if permission is None:
            db.add(
                Permission(
                    name=permission_name,
                )
            )

    db.commit()


def seed_role_permissions(
    db: Session,
) -> None:
    """
    Synchronize default role permissions.

    Existing role permissions are replaced with
    the permissions defined in ROLE_PERMISSIONS.

    This prevents obsolete permissions from
    remaining assigned after the RBAC policy
    changes.
    """

    for (
        role_name,
        permission_names,
    ) in ROLE_PERMISSIONS.items():

        role = (
            db.query(Role)
            .filter(
                Role.name == role_name
            )
            .first()
        )

        if role is None:
            raise RuntimeError(
                f"Required role '{role_name}' "
                "does not exist"
            )

        permissions = (
            db.query(Permission)
            .filter(
                Permission.name.in_(
                    permission_names
                )
            )
            .all()
        )

        found_names = {
            permission.name
            for permission in permissions
        }

        missing_names = (
            set(permission_names)
            - found_names
        )

        if missing_names:
            raise RuntimeError(
                "Missing required permissions: "
                + ", ".join(
                    sorted(missing_names)
                )
            )

        role.permissions = permissions

    db.commit()