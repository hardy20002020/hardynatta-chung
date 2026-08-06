from datetime import date
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import delete

from app.core.security import (
    create_access_token,
    hash_password,
)
from app.db.session import SessionLocal
from app.main import app
from app.models.audit_log import AuditLog
from app.models.competition import Competition
from app.models.competition_round import CompetitionRound
from app.models.competition_round_judge import (
    CompetitionRoundJudge,
)
from app.models.role import Role
from app.models.user import User
from app.models.user_session import UserSession


client = TestClient(app)


# ==========================================================
# AUTHORIZATION
# ==========================================================

def authorization_header(token):
    return {
        "Authorization": f"Bearer {token}",
    }


# ==========================================================
# TEST DATA HELPERS
# ==========================================================

def create_test_user(
    db,
    role_name: str,
    *,
    is_active: bool = True,
):
    role = (
        db.query(Role)
        .filter(
            Role.name == role_name
        )
        .one()
    )

    email = (
        "competition-round-judge-api-test-"
        f"{role_name}-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=(
            "Competition Round Judge API Test "
            f"{role_name.title()}"
        ),
        email=email,
        password=hash_password(
            "MAJE-Round-Judge-2026!"
        ),
        role_id=role.id,
        is_active=is_active,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": role.name,
            "role_id": role.id,
            "token_version": user.token_version,
        }
    )

    return user, token


def create_test_competition(
    db,
    code: str,
):
    competition = Competition(
        name="MAJE Round Judge Test Competition",
        code=code,
        year=2026,
        age_reference_date=date(
            2026,
            1,
            1,
        ),
    )

    db.add(competition)
    db.commit()
    db.refresh(competition)

    return competition


def create_test_round(
    db,
    competition_id: int,
    code: str,
):
    competition_round = CompetitionRound(
        competition_id=competition_id,
        code=code,
        name="Round Judge Test Round",
        description="Round judge API test",
        sort_order=10,
        is_active=True,
    )

    db.add(competition_round)
    db.commit()
    db.refresh(competition_round)

    return competition_round


def create_round_judge_context(
    db,
    suffix: str,
):
    competition = create_test_competition(
        db,
        (
            "RJ-"
            f"{suffix}-"
            f"{uuid4().hex[:8]}"
        ),
    )

    competition_round = create_test_round(
        db,
        competition.id,
        (
            "R-"
            f"{suffix}-"
            f"{uuid4().hex[:6]}"
        ),
    )

    return {
        "competition": competition,
        "round": competition_round,
    }


# ==========================================================
# CLEANUP
# ==========================================================

def cleanup_test_data(
    db,
    user_ids,
    competition_ids,
):
    db.rollback()

    if competition_ids:
        round_ids = [
            round_id
            for (round_id,) in (
                db.query(
                    CompetitionRound.id
                )
                .filter(
                    CompetitionRound.competition_id.in_(
                        competition_ids
                    )
                )
                .all()
            )
        ]

        if round_ids:
            db.execute(
                delete(
                    CompetitionRoundJudge
                ).where(
                    CompetitionRoundJudge
                    .competition_round_id.in_(
                        round_ids
                    )
                )
            )

        db.execute(
            delete(
                CompetitionRound
            ).where(
                CompetitionRound.competition_id.in_(
                    competition_ids
                )
            )
        )

        db.execute(
            delete(
                Competition
            ).where(
                Competition.id.in_(
                    competition_ids
                )
            )
        )

    if user_ids:
        db.execute(
            delete(
                CompetitionRoundJudge
            ).where(
                CompetitionRoundJudge.user_id.in_(
                    user_ids
                )
            )
        )

        db.execute(
            delete(
                UserSession
            ).where(
                UserSession.user_id.in_(
                    user_ids
                )
            )
        )

        db.execute(
            delete(
                AuditLog
            ).where(
                AuditLog.user_id.in_(
                    user_ids
                )
            )
        )

        db.execute(
            delete(
                User
            ).where(
                User.id.in_(
                    user_ids
                )
            )
        )

    db.commit()


# ==========================================================
# TEST 1 - CRUD, FILTERS, DUPLICATE
# ==========================================================

def test_competition_round_judge_crud_and_filters():
    db = SessionLocal()

    user_ids = []
    competition_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(
            admin.id
        )

        judge_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.append(
            judge_user.id
        )

        context = create_round_judge_context(
            db,
            "CRUD",
        )

        competition_ids.append(
            context["competition"].id
        )

        competition_round = context[
            "round"
        ]

        # --------------------------------------------------
        # CREATE
        # --------------------------------------------------

        response = client.post(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_round_id": (
                    competition_round.id
                ),
                "user_id": judge_user.id,
                "judge_order": 1,
                "status": "assigned",
            },
        )

        assert response.status_code == 201

        data = response.json()

        assert data[
            "competition_round_id"
        ] == competition_round.id

        assert data[
            "user_id"
        ] == judge_user.id

        assert data[
            "judge_order"
        ] == 1

        assert data[
            "status"
        ] == "assigned"

        judge_id = data["id"]

        # --------------------------------------------------
        # DUPLICATE ASSIGNMENT
        # --------------------------------------------------

        response = client.post(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_round_id": (
                    competition_round.id
                ),
                "user_id": judge_user.id,
                "judge_order": 2,
                "status": "assigned",
            },
        )

        assert response.status_code == 409

        assert response.json()["message"] == (
            "User already assigned to "
            "competition round"
        )

        # --------------------------------------------------
        # DETAIL
        # --------------------------------------------------

        response = client.get(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == judge_id
        assert data["user_id"] == judge_user.id

        # --------------------------------------------------
        # LIST
        # --------------------------------------------------

        response = client.get(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        assert any(
            item["id"] == judge_id
            for item in response.json()
        )

        # --------------------------------------------------
        # FILTER BY ROUND
        # --------------------------------------------------

        response = client.get(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            params={
                "competition_round_id": (
                    competition_round.id
                ),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == judge_id

        # --------------------------------------------------
        # FILTER BY USER
        # --------------------------------------------------

        response = client.get(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            params={
                "user_id": judge_user.id,
            },
        )

        assert response.status_code == 200

        assert any(
            item["id"] == judge_id
            for item in response.json()
        )

        # --------------------------------------------------
        # FILTER BY ROUND + USER
        # --------------------------------------------------

        response = client.get(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            params={
                "competition_round_id": (
                    competition_round.id
                ),
                "user_id": judge_user.id,
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == judge_id

        # --------------------------------------------------
        # UPDATE
        # --------------------------------------------------

        response = client.put(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                token
            ),
            json={
                "judge_order": 5,
                "status": "confirmed",
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert data["judge_order"] == 5
        assert data["status"] == "confirmed"

        # --------------------------------------------------
        # DELETE
        # --------------------------------------------------

        response = client.delete(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        assert response.json()["success"] is True

        # --------------------------------------------------
        # DETAIL AFTER DELETE
        # --------------------------------------------------

        response = client.get(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_ids,
        )

        db.close()


# ==========================================================
# TEST 2 - INACTIVE USER CANNOT BE JUDGE
# ==========================================================

def test_round_judge_rejects_inactive_user():
    db = SessionLocal()

    user_ids = []
    competition_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(
            admin.id
        )

        inactive_user, _ = create_test_user(
            db,
            "user",
            is_active=False,
        )

        user_ids.append(
            inactive_user.id
        )

        context = create_round_judge_context(
            db,
            "INACTIVE",
        )

        competition_ids.append(
            context["competition"].id
        )

        response = client.post(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_round_id": (
                    context["round"].id
                ),
                "user_id": inactive_user.id,
                "judge_order": 1,
                "status": "assigned",
            },
        )

        assert response.status_code == 400

        assert response.json()["message"] == (
            "User must be active to be assigned "
            "as competition round judge"
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_ids,
        )

        db.close()


# ==========================================================
# TEST 3 - MISSING DEPENDENCIES
# ==========================================================

def test_round_judge_missing_dependencies():
    db = SessionLocal()

    user_ids = []
    competition_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(
            admin.id
        )

        judge_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.append(
            judge_user.id
        )

        context = create_round_judge_context(
            db,
            "MISSING",
        )

        competition_ids.append(
            context["competition"].id
        )

        competition_round = context[
            "round"
        ]

        # --------------------------------------------------
        # MISSING ROUND
        # --------------------------------------------------

        response = client.post(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_round_id": 999999999,
                "user_id": judge_user.id,
                "judge_order": 1,
                "status": "assigned",
            },
        )

        assert response.status_code == 404

        assert response.json()["message"] == (
            "Competition round not found"
        )

        # --------------------------------------------------
        # MISSING USER
        # --------------------------------------------------

        response = client.post(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_round_id": (
                    competition_round.id
                ),
                "user_id": 999999999,
                "judge_order": 1,
                "status": "assigned",
            },
        )

        assert response.status_code == 404

        assert response.json()["message"] == (
            "User not found"
        )

        # --------------------------------------------------
        # FILTER MISSING ROUND
        # --------------------------------------------------

        response = client.get(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            params={
                "competition_round_id": (
                    999999999
                ),
            },
        )

        assert response.status_code == 404

        # --------------------------------------------------
        # FILTER MISSING USER
        # --------------------------------------------------

        response = client.get(
            "/competition-round-judges/",
            headers=authorization_header(
                token
            ),
            params={
                "user_id": 999999999,
            },
        )

        assert response.status_code == 404

        # --------------------------------------------------
        # DETAIL MISSING JUDGE
        # --------------------------------------------------

        response = client.get(
            (
                "/competition-round-judges/"
                "999999999"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

        # --------------------------------------------------
        # UPDATE MISSING JUDGE
        # --------------------------------------------------

        response = client.put(
            (
                "/competition-round-judges/"
                "999999999"
            ),
            headers=authorization_header(
                token
            ),
            json={
                "judge_order": 2,
                "status": "confirmed",
            },
        )

        assert response.status_code == 404

        # --------------------------------------------------
        # DELETE MISSING JUDGE
        # --------------------------------------------------

        response = client.delete(
            (
                "/competition-round-judges/"
                "999999999"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_ids,
        )

        db.close()


# ==========================================================
# TEST 4 - MANAGER IS READ ONLY
# ==========================================================

def test_round_judge_manager_is_read_only():
    db = SessionLocal()

    user_ids = []
    competition_ids = []

    try:
        admin, admin_token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(
            admin.id
        )

        manager, manager_token = (
            create_test_user(
                db,
                "manager",
            )
        )

        user_ids.append(
            manager.id
        )

        judge_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.append(
            judge_user.id
        )

        context = create_round_judge_context(
            db,
            "MANAGER",
        )

        competition_ids.append(
            context["competition"].id
        )

        competition_round = context[
            "round"
        ]

        # Admin creates the judge assignment.
        response = client.post(
            "/competition-round-judges/",
            headers=authorization_header(
                admin_token
            ),
            json={
                "competition_round_id": (
                    competition_round.id
                ),
                "user_id": judge_user.id,
                "judge_order": 1,
                "status": "assigned",
            },
        )

        assert response.status_code == 201

        judge_id = response.json()["id"]

        # --------------------------------------------------
        # MANAGER CAN LIST
        # --------------------------------------------------

        response = client.get(
            "/competition-round-judges/",
            headers=authorization_header(
                manager_token
            ),
        )

        assert response.status_code == 200

        # --------------------------------------------------
        # MANAGER CAN READ DETAIL
        # --------------------------------------------------

        response = client.get(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                manager_token
            ),
        )

        assert response.status_code == 200

        # --------------------------------------------------
        # MANAGER CANNOT CREATE
        # --------------------------------------------------

        response = client.post(
            "/competition-round-judges/",
            headers=authorization_header(
                manager_token
            ),
            json={
                "competition_round_id": (
                    competition_round.id
                ),
                "user_id": manager.id,
                "judge_order": 2,
                "status": "assigned",
            },
        )

        assert response.status_code == 403

        # --------------------------------------------------
        # MANAGER CANNOT UPDATE
        # --------------------------------------------------

        response = client.put(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                manager_token
            ),
            json={
                "judge_order": 10,
                "status": "confirmed",
            },
        )

        assert response.status_code == 403

        # --------------------------------------------------
        # MANAGER CANNOT DELETE
        # --------------------------------------------------

        response = client.delete(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                manager_token
            ),
        )

        assert response.status_code == 403

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_ids,
        )

        db.close()


# ==========================================================
# TEST 5 - USER HAS NO ACCESS
# ==========================================================

def test_round_judge_user_has_no_access():
    db = SessionLocal()

    user_ids = []
    competition_ids = []

    try:
        admin, admin_token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(
            admin.id
        )

        regular_user, user_token = (
            create_test_user(
                db,
                "user",
            )
        )

        user_ids.append(
            regular_user.id
        )

        judge_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.append(
            judge_user.id
        )

        context = create_round_judge_context(
            db,
            "USER",
        )

        competition_ids.append(
            context["competition"].id
        )

        competition_round = context[
            "round"
        ]

        # Admin creates assignment for RBAC checks.
        response = client.post(
            "/competition-round-judges/",
            headers=authorization_header(
                admin_token
            ),
            json={
                "competition_round_id": (
                    competition_round.id
                ),
                "user_id": judge_user.id,
                "judge_order": 1,
                "status": "assigned",
            },
        )

        assert response.status_code == 201

        judge_id = response.json()["id"]

        # --------------------------------------------------
        # USER CANNOT LIST
        # --------------------------------------------------

        response = client.get(
            "/competition-round-judges/",
            headers=authorization_header(
                user_token
            ),
        )

        assert response.status_code == 403

        # --------------------------------------------------
        # USER CANNOT READ DETAIL
        # --------------------------------------------------

        response = client.get(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                user_token
            ),
        )

        assert response.status_code == 403

        # --------------------------------------------------
        # USER CANNOT CREATE
        # --------------------------------------------------

        response = client.post(
            "/competition-round-judges/",
            headers=authorization_header(
                user_token
            ),
            json={
                "competition_round_id": (
                    competition_round.id
                ),
                "user_id": regular_user.id,
                "judge_order": 2,
                "status": "assigned",
            },
        )

        assert response.status_code == 403

        # --------------------------------------------------
        # USER CANNOT UPDATE
        # --------------------------------------------------

        response = client.put(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                user_token
            ),
            json={
                "judge_order": 2,
                "status": "confirmed",
            },
        )

        assert response.status_code == 403

        # --------------------------------------------------
        # USER CANNOT DELETE
        # --------------------------------------------------

        response = client.delete(
            (
                "/competition-round-judges/"
                f"{judge_id}"
            ),
            headers=authorization_header(
                user_token
            ),
        )

        assert response.status_code == 403

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_ids,
        )

        db.close()