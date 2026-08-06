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
from app.models.competition_round import (
    CompetitionRound,
)
from app.models.role import Role
from app.models.user import User
from app.models.user_session import UserSession


client = TestClient(app)


def authorization_header(token):
    return {
        "Authorization": f"Bearer {token}",
    }


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
        "competition-round-api-test-"
        f"{role_name}-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=(
            "Competition Round API Test "
            f"{role_name.title()}"
        ),
        email=email,
        password=hash_password(
            "MAJE-Competition-Round-2026!"
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
        name="MAJE Competition Round Test",
        code=code,
        year=2026,
    )

    db.add(competition)
    db.commit()
    db.refresh(competition)

    return competition


def cleanup_test_data(
    db,
    user_ids,
    competition_codes,
):
    db.rollback()

    if competition_codes:
        competition_ids = [
            competition_id
            for (competition_id,) in (
                db.query(Competition.id)
                .filter(
                    Competition.code.in_(
                        competition_codes
                    )
                )
                .all()
            )
        ]

        if competition_ids:
            db.execute(
                delete(CompetitionRound).where(
                    CompetitionRound.competition_id.in_(
                        competition_ids
                    )
                )
            )

        db.execute(
            delete(Competition).where(
                Competition.code.in_(
                    competition_codes
                )
            )
        )

    if user_ids:
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


def test_admin_competition_round_crud():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-ROUND-CRUD-"
        f"{uuid4().hex[:12].upper()}"
    )

    competition_codes = [
        competition_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        competition = create_test_competition(
            db,
            competition_code,
        )

        headers = authorization_header(
            token
        )

        create_response = client.post(
            "/competition-rounds/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "code": "MANDARIN",
                "name": "Mandarin Song",
                "description": (
                    "Mandarin singing round"
                ),
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert create_response.status_code == 201

        created = create_response.json()

        assert (
            created["competition_id"]
            == competition.id
        )
        assert created["code"] == "MANDARIN"
        assert created["name"] == "Mandarin Song"
        assert (
            created["description"]
            == "Mandarin singing round"
        )
        assert created["sort_order"] == 10
        assert created["is_active"] is True

        round_id = created["id"]

        list_response = client.get(
            "/competition-rounds/",
            headers=headers,
        )

        assert list_response.status_code == 200

        assert any(
            round["id"] == round_id
            for round in list_response.json()
        )

        detail_response = client.get(
            (
                "/competition-rounds/"
                f"{round_id}"
            ),
            headers=headers,
        )

        assert detail_response.status_code == 200

        assert (
            detail_response.json()["id"]
            == round_id
        )

        update_response = client.put(
            (
                "/competition-rounds/"
                f"{round_id}"
            ),
            headers=headers,
            json={
                "code": "POP",
                "name": "Mandarin Pop",
                "description": (
                    "Mandarin pop song round"
                ),
                "sort_order": 20,
                "is_active": False,
            },
        )

        assert update_response.status_code == 200

        updated = update_response.json()

        assert updated["code"] == "POP"
        assert updated["name"] == "Mandarin Pop"
        assert (
            updated["description"]
            == "Mandarin pop song round"
        )
        assert updated["sort_order"] == 20
        assert updated["is_active"] is False

        delete_response = client.delete(
            (
                "/competition-rounds/"
                f"{round_id}"
            ),
            headers=headers,
        )

        assert delete_response.status_code == 200

        assert delete_response.json() == {
            "success": True,
            "message": (
                "Competition round deleted "
                "successfully"
            ),
        }

        missing_response = client.get(
            (
                "/competition-rounds/"
                f"{round_id}"
            ),
            headers=headers,
        )

        assert missing_response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_filter_rounds_by_competition():
    db = SessionLocal()

    user_ids = []

    first_code = (
        "TEST-ROUND-FILTER-A-"
        f"{uuid4().hex[:10].upper()}"
    )

    second_code = (
        "TEST-ROUND-FILTER-B-"
        f"{uuid4().hex[:10].upper()}"
    )

    competition_codes = [
        first_code,
        second_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        first_competition = (
            create_test_competition(
                db,
                first_code,
            )
        )

        second_competition = (
            create_test_competition(
                db,
                second_code,
            )
        )

        first_round = CompetitionRound(
            competition_id=first_competition.id,
            code="CAT-A",
            name="Round A",
            description="First round",
            sort_order=10,
        )

        second_round = CompetitionRound(
            competition_id=second_competition.id,
            code="CAT-B",
            name="Round B",
            description="Second round",
            sort_order=20,
        )

        db.add_all(
            [
                first_round,
                second_round,
            ]
        )

        db.commit()
        db.refresh(first_round)
        db.refresh(second_round)

        response = client.get(
            (
                "/competition-rounds/"
                f"?competition_id={first_competition.id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        rounds = response.json()

        assert len(rounds) == 1

        assert (
            rounds[0]["id"]
            == first_round.id
        )

        assert (
            rounds[0]["competition_id"]
            == first_competition.id
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_round_sort_order():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-ROUND-SORT-"
        f"{uuid4().hex[:12].upper()}"
    )

    competition_codes = [
        competition_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        competition = create_test_competition(
            db,
            competition_code,
        )

        rounds = [
            CompetitionRound(
                competition_id=competition.id,
                code="THIRD",
                name="Third",
                sort_order=30,
            ),
            CompetitionRound(
                competition_id=competition.id,
                code="FIRST",
                name="First",
                sort_order=10,
            ),
            CompetitionRound(
                competition_id=competition.id,
                code="SECOND",
                name="Second",
                sort_order=20,
            ),
        ]

        db.add_all(rounds)
        db.commit()

        response = client.get(
            (
                "/competition-rounds/"
                f"?competition_id={competition.id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        result = response.json()

        assert len(result) == 3

        assert [
            round["code"]
            for round in result
        ] == [
            "FIRST",
            "SECOND",
            "THIRD",
        ]

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_duplicate_round_code_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-ROUND-DUP-"
        f"{uuid4().hex[:12].upper()}"
    )

    competition_codes = [
        competition_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        competition = create_test_competition(
            db,
            competition_code,
        )

        headers = authorization_header(
            token
        )

        first_response = client.post(
            "/competition-rounds/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "code": "SOLO",
                "name": "Solo",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert first_response.status_code == 201

        duplicate_response = client.post(
            "/competition-rounds/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "code": "SOLO",
                "name": "Duplicate Solo",
                "description": None,
                "sort_order": 20,
                "is_active": True,
            },
        )

        assert duplicate_response.status_code == 409

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_same_round_code_allowed_in_different_competitions():
    db = SessionLocal()

    user_ids = []

    first_code = (
        "TEST-ROUND-SAME-A-"
        f"{uuid4().hex[:10].upper()}"
    )

    second_code = (
        "TEST-ROUND-SAME-B-"
        f"{uuid4().hex[:10].upper()}"
    )

    competition_codes = [
        first_code,
        second_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        first_competition = (
            create_test_competition(
                db,
                first_code,
            )
        )

        second_competition = (
            create_test_competition(
                db,
                second_code,
            )
        )

        headers = authorization_header(
            token
        )

        first_response = client.post(
            "/competition-rounds/",
            headers=headers,
            json={
                "competition_id": (
                    first_competition.id
                ),
                "code": "SOLO",
                "name": "Solo",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/competition-rounds/",
            headers=headers,
            json={
                "competition_id": (
                    second_competition.id
                ),
                "code": "SOLO",
                "name": "Solo",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert second_response.status_code == 201

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_duplicate_round_code_on_update_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-ROUND-UPDATE-DUP-"
        f"{uuid4().hex[:10].upper()}"
    )

    competition_codes = [
        competition_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        competition = create_test_competition(
            db,
            competition_code,
        )

        first_round = CompetitionRound(
            competition_id=competition.id,
            code="FIRST",
            name="First Round",
            sort_order=10,
        )

        second_round = CompetitionRound(
            competition_id=competition.id,
            code="SECOND",
            name="Second Round",
            sort_order=20,
        )

        db.add_all(
            [
                first_round,
                second_round,
            ]
        )

        db.commit()
        db.refresh(first_round)
        db.refresh(second_round)

        response = client.put(
            (
                "/competition-rounds/"
                f"{second_round.id}"
            ),
            headers=authorization_header(
                token
            ),
            json={
                "code": "FIRST",
                "name": "Duplicate",
                "description": None,
                "sort_order": 30,
                "is_active": True,
            },
        )

        assert response.status_code == 409

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_create_round_for_missing_competition_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.post(
            "/competition-rounds/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": 2147483647,
                "code": "MISSING",
                "name": "Missing Competition",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_filter_missing_competition_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.get(
            (
                "/competition-rounds/"
                "?competition_id=2147483647"
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
            [],
        )

        db.close()


def test_competition_round_not_found_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.get(
            "/competition-rounds/2147483647",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_update_missing_round_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.put(
            "/competition-rounds/2147483647",
            headers=authorization_header(
                token
            ),
            json={
                "code": "MISSING",
                "name": "Missing Round",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_delete_missing_round_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.delete(
            "/competition-rounds/2147483647",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_can_read_competition_rounds():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.get(
            "/competition-rounds/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_create_competition_round():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.post(
            "/competition-rounds/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": 2147483647,
                "code": "FORBIDDEN",
                "name": "Forbidden",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_round.create' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_update_competition_round():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.put(
            "/competition-rounds/2147483647",
            headers=authorization_header(
                token
            ),
            json={
                "code": "FORBIDDEN",
                "name": "Forbidden",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_round.update' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_delete_competition_round():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.delete(
            "/competition-rounds/2147483647",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_round.delete' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_user_cannot_read_competition_rounds():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        user_ids.append(user.id)

        response = client.get(
            "/competition-rounds/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_round.read' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()
