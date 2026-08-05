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
from app.models.competition_group import CompetitionGroup
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
        "competition-group-api-test-"
        f"{role_name}-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=(
            "Competition Group API Test "
            f"{role_name.title()}"
        ),
        email=email,
        password=hash_password(
            "MAJE-Competition-Group-2026!"
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
        name="MAJE Competition Group Test",
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
                delete(CompetitionGroup).where(
                    CompetitionGroup.competition_id.in_(
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


def test_admin_competition_group_crud():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-GROUP-CRUD-"
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
            "/competition-groups/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "code": "GA",
                "name": "Anak-Anak",
                "sort_order": 10,
            },
        )

        assert create_response.status_code == 201

        created = create_response.json()

        assert (
            created["competition_id"]
            == competition.id
        )
        assert created["code"] == "GA"
        assert created["name"] == "Anak-Anak"
        assert created["sort_order"] == 10
        assert created["is_active"] is True

        group_id = created["id"]

        list_response = client.get(
            "/competition-groups/",
            headers=headers,
        )

        assert list_response.status_code == 200

        assert any(
            group["id"] == group_id
            for group in list_response.json()
        )

        detail_response = client.get(
            f"/competition-groups/{group_id}",
            headers=headers,
        )

        assert detail_response.status_code == 200
        assert (
            detail_response.json()["id"]
            == group_id
        )

        update_response = client.put(
            f"/competition-groups/{group_id}",
            headers=headers,
            json={
                "code": "GR",
                "name": "Remaja",
                "sort_order": 20,
                "is_active": False,
            },
        )

        assert update_response.status_code == 200

        updated = update_response.json()

        assert updated["code"] == "GR"
        assert updated["name"] == "Remaja"
        assert updated["sort_order"] == 20
        assert updated["is_active"] is False

        delete_response = client.delete(
            f"/competition-groups/{group_id}",
            headers=headers,
        )

        assert delete_response.status_code == 200
        assert delete_response.json() == {
            "success": True,
            "message": (
                "Competition group deleted "
                "successfully"
            ),
        }

        missing_response = client.get(
            f"/competition-groups/{group_id}",
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


def test_filter_groups_by_competition():
    db = SessionLocal()

    user_ids = []

    first_code = (
        "TEST-GROUP-FILTER-A-"
        f"{uuid4().hex[:10].upper()}"
    )

    second_code = (
        "TEST-GROUP-FILTER-B-"
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

        first_group = CompetitionGroup(
            competition_id=first_competition.id,
            code="GA",
            name="Anak-Anak",
            sort_order=10,
        )

        second_group = CompetitionGroup(
            competition_id=second_competition.id,
            code="GR",
            name="Remaja",
            sort_order=20,
        )

        db.add_all(
            [
                first_group,
                second_group,
            ]
        )
        db.commit()
        db.refresh(first_group)
        db.refresh(second_group)

        response = client.get(
            (
                "/competition-groups/"
                f"?competition_id={first_competition.id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        groups = response.json()

        assert len(groups) == 1
        assert groups[0]["id"] == first_group.id
        assert (
            groups[0]["competition_id"]
            == first_competition.id
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_duplicate_group_code_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-GROUP-DUP-"
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
            "/competition-groups/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "code": "GD",
                "name": "Dewasa",
                "sort_order": 30,
            },
        )

        assert first_response.status_code == 201

        duplicate_response = client.post(
            "/competition-groups/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "code": "GD",
                "name": "Duplicate Dewasa",
                "sort_order": 31,
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


def test_same_group_code_allowed_in_different_competitions():
    db = SessionLocal()

    user_ids = []

    first_code = (
        "TEST-GROUP-SAME-A-"
        f"{uuid4().hex[:10].upper()}"
    )

    second_code = (
        "TEST-GROUP-SAME-B-"
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
            "/competition-groups/",
            headers=headers,
            json={
                "competition_id": (
                    first_competition.id
                ),
                "code": "EG",
                "name": "Evergreen",
                "sort_order": 40,
            },
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/competition-groups/",
            headers=headers,
            json={
                "competition_id": (
                    second_competition.id
                ),
                "code": "EG",
                "name": "Evergreen",
                "sort_order": 40,
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


def test_create_group_for_missing_competition_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.post(
            "/competition-groups/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": 2147483647,
                "code": "WB",
                "name": "WULAN Bahagia",
                "sort_order": 50,
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
                "/competition-groups/"
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


def test_competition_group_not_found_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.get(
            "/competition-groups/2147483647",
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


def test_manager_can_read_competition_groups():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.get(
            "/competition-groups/",
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


def test_manager_cannot_create_competition_group():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.post(
            "/competition-groups/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": 2147483647,
                "code": "GA",
                "name": "Anak-Anak",
                "sort_order": 10,
            },
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_group.create' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_update_competition_group():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.put(
            "/competition-groups/2147483647",
            headers=authorization_header(
                token
            ),
            json={
                "code": "GD",
                "name": "Dewasa",
                "sort_order": 30,
                "is_active": True,
            },
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_group.update' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_delete_competition_group():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.delete(
            "/competition-groups/2147483647",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_group.delete' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_user_cannot_read_competition_groups():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        user_ids.append(user.id)

        response = client.get(
            "/competition-groups/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_group.read' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()