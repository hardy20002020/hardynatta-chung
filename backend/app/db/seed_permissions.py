from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.role import Role


PERMISSIONS = [

    # ======================================================
    # Users
    # ======================================================

    "user.create",
    "user.read",
    "user.update",
    "user.delete",


    # ======================================================
    # Provinces
    # ======================================================

    "province.create",
    "province.read",
    "province.update",
    "province.delete",


    # ======================================================
    # Cities
    # ======================================================

    "city.create",
    "city.read",
    "city.update",
    "city.delete",


    # ======================================================
    # Dashboard
    # ======================================================

    "dashboard.read",


    # ======================================================
    # Competitions
    # ======================================================

    "competition.create",
    "competition.read",
    "competition.update",
    "competition.delete",


    # ======================================================
    # Competition Groups
    # ======================================================

    "competition_group.create",
    "competition_group.read",
    "competition_group.update",
    "competition_group.delete",


    # ======================================================
    # Competition Categories
    # ======================================================

    "competition_category.create",
    "competition_category.read",
    "competition_category.update",
    "competition_category.delete",


    # ======================================================
    # Competition Rounds
    # ======================================================

    "competition_round.create",
    "competition_round.read",
    "competition_round.update",
    "competition_round.delete",


    # ======================================================
    # Competition Round Entries
    # ======================================================

    "competition_round_entry.create",
    "competition_round_entry.read",
    "competition_round_entry.update",
    "competition_round_entry.delete",


    # ======================================================
    # Competition Round Judges
    # ======================================================

    "competition_round_judge.create",
    "competition_round_judge.read",
    "competition_round_judge.update",
    "competition_round_judge.delete",


    # ======================================================
    # Competition Scoring Criteria
    # ======================================================

    "competition_scoring_criterion.create",
    "competition_scoring_criterion.read",
    "competition_scoring_criterion.update",
    "competition_scoring_criterion.delete",


    # ======================================================
    # Competition Judge Scores
    # ======================================================

    "competition_judge_score.read",
    "competition_judge_score.submit",
    "competition_judge_score.lock",


    # ======================================================
    # Competition Judge Score Detail
    # ======================================================

    "competition_judge_score_detail.create",
    "competition_judge_score_detail.read",
    "competition_judge_score_detail.update",
    "competition_judge_score_detail.delete",


    # ======================================================
    # Competition Results
    # ======================================================

    "competition_result.read",
    "competition_result.finalize",
    "competition_result.approve",
    "competition_result.publish",


    # ======================================================
    # Competition Registrations
    # ======================================================

    "competition_registration.create",
    "competition_registration.read",
    "competition_registration.update",
    "competition_registration.delete",


    # ======================================================
    # Participants - Administration
    # ======================================================

    "participant.create",
    "participant.read",
    "participant.update",
    "participant.delete",


    # ======================================================
    # Participants - Self Service Portal
    # ======================================================

    "participant.self.create",
    "participant.self.read",
    "participant.self.update",
]


# ==========================================================
# ROLE PERMISSIONS
# ==========================================================

ROLE_PERMISSIONS = {


    # ======================================================
    # ADMIN
    # ======================================================

    "admin": PERMISSIONS,


    # ======================================================
    # MANAGER
    # ======================================================

    "manager": [

        "dashboard.read",

        "competition.read",

        "competition_group.read",

        "competition_category.read",

        "competition_round.read",

        "competition_round_entry.read",

        "competition_round_judge.read",

        "competition_scoring_criterion.read",

        "competition_judge_score.read",

        "competition_judge_score_detail.read",

        "competition_result.read",

        "competition_registration.read",

        "participant.read",
    ],


    # ======================================================
    # USER
    # ======================================================

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
    """

    for (
        role_name,
        permission_names,
    ) in ROLE_PERMISSIONS.items():

        role = (
            db.query(Role)
            .filter(
                Role.name
                == role_name
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
