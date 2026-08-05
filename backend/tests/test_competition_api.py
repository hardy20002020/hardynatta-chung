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
        "competition-api-test-"
        f"{role_name}-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=(
            "Competition API Test "
            f"{role_name.title()}"
        ),
        email=email,
        password=hash_password(
            "MAJE-Competition-2026!"
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


def cleanup_test_data(
    db,
    user_ids,
    competition_codes,
):
    db.rollback()

    if competition_codes:
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


def test_admin_competition_crud():
    db = SessionLocal()

    user_ids = []
    competition_codes = []

    code = (
        "TEST-MMS-"
        f"{uuid4().hex[:12].upper()}"
    )

    updated_code = (
        "TEST-MMS-UPDATED-"
        f"{uuid4().hex[:8].upper()}"
    )

    competition_codes.extend(
        [
            code,
            updated_code,
        ]
    )

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        headers = authorization_header(
            token
        )

        create_response = client.post(
            "/competitions/",
            headers=headers,
            json={
                "name": "MAJE Test Competition",
                "code": code,
                "year": 2026,
            },
        )

        assert create_response.status_code == 201

        created = create_response.json()

        assert created["name"] == (
            "MAJE Test Competition"
        )
        assert created["code"] == code
        assert created["year"] == 2026
        assert created["age_reference_date"] is None
        assert created["is_active"] is True

        competition_id = created["id"]

        list_response = client.get(
            "/competitions/",
            headers=headers,
        )

        assert list_response.status_code == 200

        assert any(
            competition["id"]
            == competition_id
            for competition
            in list_response.json()
        )

        detail_response = client.get(
            f"/competitions/{competition_id}",
            headers=headers,
        )

        assert detail_response.status_code == 200
        assert (
            detail_response.json()["id"]
            == competition_id
        )

        update_response = client.put(
            f"/competitions/{competition_id}",
            headers=headers,
            json={
                "name": (
                    "MAJE Test Competition Updated"
                ),
                "code": updated_code,
                "year": 2027,
                "age_reference_date": None,
                "is_active": False,
            },
        )

        assert update_response.status_code == 200

        updated = update_response.json()

        assert updated["name"] == (
            "MAJE Test Competition Updated"
        )
        assert updated["code"] == updated_code
        assert updated["year"] == 2027
        assert updated["age_reference_date"] is None
        assert updated["is_active"] is False

        delete_response = client.delete(
            f"/competitions/{competition_id}",
            headers=headers,
        )

        assert delete_response.status_code == 200
        assert delete_response.json() == {
            "success": True,
            "message": (
                "Competition deleted successfully"
            ),
        }

        missing_response = client.get(
            f"/competitions/{competition_id}",
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


def test_admin_competition_age_reference_date():
    db = SessionLocal()

    user_ids = []

    code = (
        "TEST-AGE-REF-"
        f"{uuid4().hex[:12].upper()}"
    )

    updated_code = (
        "TEST-AGE-REF-UPD-"
        f"{uuid4().hex[:8].upper()}"
    )

    competition_codes = [
        code,
        updated_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        headers = authorization_header(
            token
        )

        create_response = client.post(
            "/competitions/",
            headers=headers,
            json={
                "name": (
                    "MAJE Age Reference Test"
                ),
                "code": code,
                "year": 2026,
                "age_reference_date": (
                    "2026-06-30"
                ),
            },
        )

        assert create_response.status_code == 201

        created = create_response.json()

        assert created["age_reference_date"] == (
            "2026-06-30"
        )

        competition_id = created["id"]

        detail_response = client.get(
            f"/competitions/{competition_id}",
            headers=headers,
        )

        assert detail_response.status_code == 200

        assert (
            detail_response.json()[
                "age_reference_date"
            ]
            == "2026-06-30"
        )

        update_response = client.put(
            f"/competitions/{competition_id}",
            headers=headers,
            json={
                "name": (
                    "MAJE Age Reference Updated"
                ),
                "code": updated_code,
                "year": 2027,
                "age_reference_date": (
                    "2027-01-01"
                ),
                "is_active": True,
            },
        )

        assert update_response.status_code == 200

        updated = update_response.json()

        assert updated["age_reference_date"] == (
            "2027-01-01"
        )

        delete_response = client.delete(
            f"/competitions/{competition_id}",
            headers=headers,
        )

        assert delete_response.status_code == 200

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_duplicate_competition_code_is_rejected():
    db = SessionLocal()

    user_ids = []

    code = (
        "TEST-DUPLICATE-"
        f"{uuid4().hex[:12].upper()}"
    )

    competition_codes = [
        code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        headers = authorization_header(
            token
        )

        first_response = client.post(
            "/competitions/",
            headers=headers,
            json={
                "name": "First Competition",
                "code": code,
                "year": 2026,
            },
        )

        assert first_response.status_code == 201

        duplicate_response = client.post(
            "/competitions/",
            headers=headers,
            json={
                "name": "Duplicate Competition",
                "code": code,
                "year": 2026,
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


def test_competition_not_found_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.get(
            "/competitions/2147483647",
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


def test_manager_can_read_competitions():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        headers = authorization_header(
            token
        )

        list_response = client.get(
            "/competitions/",
            headers=headers,
        )

        assert list_response.status_code == 200

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_create_competition():
    db = SessionLocal()

    user_ids = []

    code = (
        "TEST-MANAGER-"
        f"{uuid4().hex[:12].upper()}"
    )

    competition_codes = [
        code,
    ]

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.post(
            "/competitions/",
            headers=authorization_header(
                token
            ),
            json={
                "name": (
                    "Manager Forbidden Competition"
                ),
                "code": code,
                "year": 2026,
            },
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition.create' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_manager_cannot_update_competition():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.put(
            "/competitions/2147483647",
            headers=authorization_header(
                token
            ),
            json={
                "name": (
                    "Manager Forbidden Update"
                ),
                "code": "TEST-MANAGER-UPDATE",
                "year": 2026,
                "age_reference_date": None,
                "is_active": True,
            },
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition.update' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_delete_competition():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.delete(
            "/competitions/2147483647",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition.delete' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_user_cannot_read_competitions():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        user_ids.append(user.id)

        response = client.get(
            "/competitions/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition.read' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()