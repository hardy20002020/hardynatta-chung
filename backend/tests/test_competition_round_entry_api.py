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
from app.models.competition_category import (
    CompetitionCategory,
)
from app.models.competition_group import CompetitionGroup
from app.models.competition_registration import (
    CompetitionRegistration,
)
from app.models.competition_round import CompetitionRound
from app.models.competition_round_entry import (
    CompetitionRoundEntry,
)
from app.models.participant import Participant
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
):
    role = (
        db.query(Role)
        .filter(Role.name == role_name)
        .one()
    )

    email = (
        "competition-round-entry-api-test-"
        f"{role_name}-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=(
            "Competition Round Entry API Test "
            f"{role_name.title()}"
        ),
        email=email,
        password=hash_password(
            "MAJE-Round-Entry-2026!"
        ),
        role_id=role.id,
        is_active=True,
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
        name="MAJE Round Entry Test Competition",
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


def create_test_group(
    db,
    competition_id: int,
    code: str,
):
    group = CompetitionGroup(
        competition_id=competition_id,
        code=code,
        name="Round Entry Test Group",
        min_age=None,
        max_age=None,
        sort_order=10,
        is_active=True,
    )

    db.add(group)
    db.commit()
    db.refresh(group)

    return group


def create_test_category(
    db,
    competition_id: int,
    code: str,
):
    category = CompetitionCategory(
        competition_id=competition_id,
        code=code,
        name="Round Entry Test Category",
        description="Round entry API test",
        sort_order=10,
        is_active=True,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def create_test_round(
    db,
    competition_id: int,
    code: str,
):
    competition_round = CompetitionRound(
        competition_id=competition_id,
        code=code,
        name="Round Entry Test Round",
        description="Round entry API test",
        sort_order=10,
        is_active=True,
    )

    db.add(competition_round)
    db.commit()
    db.refresh(competition_round)

    return competition_round


def create_test_participant(
    db,
    user_id: int,
):
    participant = Participant(
        user_id=user_id,
        chinese_name="Round Entry Participant",
        gender="male",
        date_of_birth=date(
            2000,
            1,
            1,
        ),
    )

    db.add(participant)
    db.commit()
    db.refresh(participant)

    return participant


def create_test_registration(
    db,
    competition,
    group,
    category,
    participant,
):
    registration = CompetitionRegistration(
        competition_id=competition.id,
        competition_group_id=group.id,
        competition_category_id=category.id,
        participant_id=participant.id,
        registration_number=(
            "RE-REG-"
            f"{uuid4().hex[:12]}"
        ),
        status="registered",
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    return registration


def create_round_entry_context(
    db,
    suffix: str,
):
    competition = create_test_competition(
        db,
        (
            "RE-"
            f"{suffix}-"
            f"{uuid4().hex[:8]}"
        ),
    )

    group = create_test_group(
        db,
        competition.id,
        (
            "G-"
            f"{suffix}-"
            f"{uuid4().hex[:6]}"
        ),
    )

    category = create_test_category(
        db,
        competition.id,
        (
            "C-"
            f"{suffix}-"
            f"{uuid4().hex[:6]}"
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

    participant_user, _ = create_test_user(
        db,
        "user",
    )

    participant = create_test_participant(
        db,
        participant_user.id,
    )

    registration = create_test_registration(
        db,
        competition,
        group,
        category,
        participant,
    )

    return {
        "competition": competition,
        "group": group,
        "category": category,
        "round": competition_round,
        "participant_user": participant_user,
        "participant": participant,
        "registration": registration,
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
                db.query(CompetitionRound.id)
                .filter(
                    CompetitionRound.competition_id.in_(
                        competition_ids
                    )
                )
                .all()
            )
        ]

        registration_ids = [
            registration_id
            for (registration_id,) in (
                db.query(
                    CompetitionRegistration.id
                )
                .filter(
                    CompetitionRegistration.competition_id.in_(
                        competition_ids
                    )
                )
                .all()
            )
        ]

        if round_ids:
            db.execute(
                delete(
                    CompetitionRoundEntry
                ).where(
                    CompetitionRoundEntry
                    .competition_round_id.in_(
                        round_ids
                    )
                )
            )

        if registration_ids:
            db.execute(
                delete(
                    CompetitionRoundEntry
                ).where(
                    CompetitionRoundEntry
                    .competition_registration_id.in_(
                        registration_ids
                    )
                )
            )

            db.execute(
                delete(
                    CompetitionRegistration
                ).where(
                    CompetitionRegistration.id.in_(
                        registration_ids
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
                CompetitionCategory
            ).where(
                CompetitionCategory.competition_id.in_(
                    competition_ids
                )
            )
        )

        db.execute(
            delete(
                CompetitionGroup
            ).where(
                CompetitionGroup.competition_id.in_(
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
                CompetitionRoundEntry
            ).where(
                CompetitionRoundEntry
                .competition_registration_id.in_(
                    db.query(
                        CompetitionRegistration.id
                    )
                    .join(
                        Participant,
                        CompetitionRegistration.participant_id
                        == Participant.id,
                    )
                    .filter(
                        Participant.user_id.in_(
                            user_ids
                        )
                    )
                )
            )
        )

        db.execute(
            delete(
                CompetitionRegistration
            ).where(
                CompetitionRegistration
                .participant_id.in_(
                    db.query(Participant.id)
                    .filter(
                        Participant.user_id.in_(
                            user_ids
                        )
                    )
                )
            )
        )

        db.execute(
            delete(Participant).where(
                Participant.user_id.in_(
                    user_ids
                )
            )
        )

        db.execute(
            delete(UserSession).where(
                UserSession.user_id.in_(
                    user_ids
                )
            )
        )

        db.execute(
            delete(AuditLog).where(
                AuditLog.user_id.in_(
                    user_ids
                )
            )
        )

        db.execute(
            delete(User).where(
                User.id.in_(
                    user_ids
                )
            )
        )

    db.commit()


# ==========================================================
# TEST 1 - CRUD AND FILTERS
# ==========================================================

def test_competition_round_entry_crud_and_filters():
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

        context = create_round_entry_context(
            db,
            "CRUD",
        )

        user_ids.append(
            context["participant_user"].id
        )

        competition_ids.append(
            context["competition"].id
        )

        payload = {
            "competition_round_id": (
                context["round"].id
            ),
            "competition_registration_id": (
                context["registration"].id
            ),
            "performance_order": 1,
            "status": "scheduled",
        }

        response = client.post(
            "/competition-round-entries/",
            json=payload,
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 201

        created = response.json()

        assert (
            created["competition_round_id"]
            == context["round"].id
        )

        assert (
            created[
                "competition_registration_id"
            ]
            == context["registration"].id
        )

        assert created["performance_order"] == 1
        assert created["status"] == "scheduled"

        entry_id = created["id"]

        response = client.get(
            (
                "/competition-round-entries/"
                f"{entry_id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200
        assert response.json()["id"] == entry_id

        response = client.get(
            "/competition-round-entries/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200
        assert any(
            item["id"] == entry_id
            for item in response.json()
        )

        response = client.get(
            "/competition-round-entries/",
            params={
                "competition_round_id": (
                    context["round"].id
                ),
            },
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200
        assert any(
            item["id"] == entry_id
            for item in response.json()
        )

        response = client.get(
            "/competition-round-entries/",
            params={
                "competition_registration_id": (
                    context["registration"].id
                ),
            },
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200
        assert any(
            item["id"] == entry_id
            for item in response.json()
        )

        response = client.get(
            "/competition-round-entries/",
            params={
                "competition_round_id": (
                    context["round"].id
                ),
                "competition_registration_id": (
                    context["registration"].id
                ),
            },
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200
        assert len(response.json()) == 1
        assert response.json()[0]["id"] == entry_id

        duplicate = client.post(
            "/competition-round-entries/",
            json=payload,
            headers=authorization_header(
                token
            ),
        )

        assert duplicate.status_code == 409

        response = client.put(
            (
                "/competition-round-entries/"
                f"{entry_id}"
            ),
            json={
                "performance_order": 5,
                "status": "completed",
            },
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200
        assert (
            response.json()["performance_order"]
            == 5
        )
        assert (
            response.json()["status"]
            == "completed"
        )

        response = client.delete(
            (
                "/competition-round-entries/"
                f"{entry_id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200
        assert response.json()["success"] is True

        response = client.get(
            (
                "/competition-round-entries/"
                f"{entry_id}"
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
# TEST 2 - CROSS COMPETITION
# ==========================================================

def test_round_entry_rejects_cross_competition():
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

        first = create_round_entry_context(
            db,
            "CROSS-A",
        )

        second = create_round_entry_context(
            db,
            "CROSS-B",
        )

        user_ids.extend(
            [
                first["participant_user"].id,
                second["participant_user"].id,
            ]
        )

        competition_ids.extend(
            [
                first["competition"].id,
                second["competition"].id,
            ]
        )

        response = client.post(
            "/competition-round-entries/",
            json={
                "competition_round_id": (
                    first["round"].id
                ),
                "competition_registration_id": (
                    second["registration"].id
                ),
                "performance_order": 1,
                "status": "scheduled",
            },
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 400
        assert response.json()["message"] == (
            "Competition round and registration "
            "must belong to the same competition"
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

def test_round_entry_missing_dependencies():
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

        context = create_round_entry_context(
            db,
            "MISSING",
        )

        user_ids.append(
            context["participant_user"].id
        )

        competition_ids.append(
            context["competition"].id
        )

        response = client.post(
            "/competition-round-entries/",
            json={
                "competition_round_id": 999999999,
                "competition_registration_id": (
                    context["registration"].id
                ),
                "performance_order": 1,
                "status": "scheduled",
            },
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404
        assert response.json()["message"] == (
            "Competition round not found"
        )

        response = client.post(
            "/competition-round-entries/",
            json={
                "competition_round_id": (
                    context["round"].id
                ),
                "competition_registration_id": (
                    999999999
                ),
                "performance_order": 1,
                "status": "scheduled",
            },
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404
        assert response.json()["message"] == (
            "Competition registration not found"
        )

        response = client.get(
            "/competition-round-entries/",
            params={
                "competition_round_id": 999999999,
            },
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

        response = client.get(
            "/competition-round-entries/",
            params={
                "competition_registration_id": (
                    999999999
                ),
            },
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
# TEST 4 - MANAGER READ ONLY
# ==========================================================

def test_round_entry_manager_is_read_only():
    db = SessionLocal()

    user_ids = []
    competition_ids = []

    try:
        admin, admin_token = create_test_user(
            db,
            "admin",
        )

        manager, manager_token = create_test_user(
            db,
            "manager",
        )

        user_ids.extend(
            [
                admin.id,
                manager.id,
            ]
        )

        context = create_round_entry_context(
            db,
            "MANAGER",
        )

        user_ids.append(
            context["participant_user"].id
        )

        competition_ids.append(
            context["competition"].id
        )

        payload = {
            "competition_round_id": (
                context["round"].id
            ),
            "competition_registration_id": (
                context["registration"].id
            ),
            "performance_order": 1,
            "status": "scheduled",
        }

        response = client.post(
            "/competition-round-entries/",
            json=payload,
            headers=authorization_header(
                admin_token
            ),
        )

        assert response.status_code == 201

        entry_id = response.json()["id"]

        response = client.get(
            "/competition-round-entries/",
            headers=authorization_header(
                manager_token
            ),
        )

        assert response.status_code == 200

        response = client.get(
            (
                "/competition-round-entries/"
                f"{entry_id}"
            ),
            headers=authorization_header(
                manager_token
            ),
        )

        assert response.status_code == 200

        response = client.post(
            "/competition-round-entries/",
            json=payload,
            headers=authorization_header(
                manager_token
            ),
        )

        assert response.status_code == 403

        response = client.put(
            (
                "/competition-round-entries/"
                f"{entry_id}"
            ),
            json={
                "performance_order": 2,
                "status": "completed",
            },
            headers=authorization_header(
                manager_token
            ),
        )

        assert response.status_code == 403

        response = client.delete(
            (
                "/competition-round-entries/"
                f"{entry_id}"
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
# TEST 5 - USER NO ACCESS
# ==========================================================

def test_round_entry_user_has_no_access():
    db = SessionLocal()

    user_ids = []
    competition_ids = []

    try:
        admin, admin_token = create_test_user(
            db,
            "admin",
        )

        user, user_token = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                user.id,
            ]
        )

        context = create_round_entry_context(
            db,
            "USER",
        )

        user_ids.append(
            context["participant_user"].id
        )

        competition_ids.append(
            context["competition"].id
        )

        payload = {
            "competition_round_id": (
                context["round"].id
            ),
            "competition_registration_id": (
                context["registration"].id
            ),
            "performance_order": 1,
            "status": "scheduled",
        }

        response = client.post(
            "/competition-round-entries/",
            json=payload,
            headers=authorization_header(
                admin_token
            ),
        )

        assert response.status_code == 201

        entry_id = response.json()["id"]

        response = client.get(
            "/competition-round-entries/",
            headers=authorization_header(
                user_token
            ),
        )

        assert response.status_code == 403

        response = client.get(
            (
                "/competition-round-entries/"
                f"{entry_id}"
            ),
            headers=authorization_header(
                user_token
            ),
        )

        assert response.status_code == 403

        response = client.post(
            "/competition-round-entries/",
            json=payload,
            headers=authorization_header(
                user_token
            ),
        )

        assert response.status_code == 403

        response = client.put(
            (
                "/competition-round-entries/"
                f"{entry_id}"
            ),
            json={
                "performance_order": 2,
                "status": "completed",
            },
            headers=authorization_header(
                user_token
            ),
        )

        assert response.status_code == 403

        response = client.delete(
            (
                "/competition-round-entries/"
                f"{entry_id}"
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
