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
from app.models.participant import Participant
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
        "participant-api-test-"
        f"{role_name}-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=(
            "Participant API Test "
            f"{role_name.title()}"
        ),
        email=email,
        password=hash_password(
            "MAJE-Participant-2026!"
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
):
    db.rollback()

    if user_ids:
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


def test_user_participant_self_service():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        user_ids.append(user.id)

        headers = authorization_header(
            token
        )

        create_response = client.post(
            "/participants/me",
            headers=headers,
            json={
                "chinese_name": "测试用户",
                "gender": "male",
                "chinese_surname_id": None,
                "ethnicity_id": None,
                "ethnicity_other": None,
            },
        )

        assert create_response.status_code == 201

        created = create_response.json()

        assert created["user_id"] == user.id
        assert created["chinese_name"] == "测试用户"
        assert created["gender"] == "male"

        participant_id = created["id"]

        get_response = client.get(
            "/participants/me",
            headers=headers,
        )

        assert get_response.status_code == 200
        assert (
            get_response.json()["id"]
            == participant_id
        )

        update_response = client.put(
            "/participants/me",
            headers=headers,
            json={
                "chinese_name": "更新用户",
                "gender": "female",
                "chinese_surname_id": None,
                "ethnicity_id": None,
                "ethnicity_other": None,
            },
        )

        assert update_response.status_code == 200

        updated = update_response.json()

        assert updated["id"] == participant_id
        assert updated["user_id"] == user.id
        assert updated["chinese_name"] == "更新用户"
        assert updated["gender"] == "female"
        assert updated["ethnicity_other"] is None

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_user_cannot_create_duplicate_self_profile():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        user_ids.append(user.id)

        headers = authorization_header(
            token
        )

        payload = {
            "chinese_name": "Duplicate Test",
            "gender": "male",
            "chinese_surname_id": None,
            "ethnicity_id": None,
            "ethnicity_other": None,
        }

        first_response = client.post(
            "/participants/me",
            headers=headers,
            json=payload,
        )

        assert first_response.status_code == 201

        duplicate_response = client.post(
            "/participants/me",
            headers=headers,
            json=payload,
        )

        assert duplicate_response.status_code == 409

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_user_self_profile_not_found_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        user_ids.append(user.id)

        response = client.get(
            "/participants/me",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_user_cannot_read_all_participants():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        user_ids.append(user.id)

        response = client.get(
            "/participants/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'participant.read' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_user_cannot_read_other_participant():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        other_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                user.id,
                other_user.id,
            ]
        )

        participant = Participant(
            user_id=other_user.id,
            chinese_name="Other Participant",
            gender="male",
        )

        db.add(participant)
        db.commit()
        db.refresh(participant)

        response = client.get(
            f"/participants/{participant.id}",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_admin_can_create_participant_for_user():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        target_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                target_user.id,
            ]
        )

        response = client.post(
            (
                "/participants/users/"
                f"{target_user.id}"
            ),
            headers=authorization_header(
                token
            ),
            json={
                "chinese_name": "Admin Created",
                "gender": "male",
                "chinese_surname_id": None,
                "ethnicity_id": None,
                "ethnicity_other": None,
            },
        )

        assert response.status_code == 201

        created = response.json()

        assert (
            created["user_id"]
            == target_user.id
        )

        assert created["gender"] == "male"

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_admin_can_read_all_participants():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.get(
            "/participants/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200
        assert isinstance(
            response.json(),
            list,
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_admin_can_update_participant():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        target_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                target_user.id,
            ]
        )

        participant = Participant(
            user_id=target_user.id,
            chinese_name="Before Update",
            gender="male",
        )

        db.add(participant)
        db.commit()
        db.refresh(participant)

        response = client.put(
            f"/participants/{participant.id}",
            headers=authorization_header(
                token
            ),
            json={
                "chinese_name": "After Update",
                "gender": "female",
                "chinese_surname_id": None,
                "ethnicity_id": None,
                "ethnicity_other": None,
            },
        )

        assert response.status_code == 200

        updated = response.json()

        assert (
            updated["chinese_name"]
            == "After Update"
        )

        assert updated["gender"] == "female"

        assert (
            updated["ethnicity_other"]
            is None
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_admin_can_delete_participant():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        target_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                target_user.id,
            ]
        )

        participant = Participant(
            user_id=target_user.id,
            chinese_name="Delete Test",
            gender="male",
        )

        db.add(participant)
        db.commit()
        db.refresh(participant)

        participant_id = participant.id

        response = client.delete(
            f"/participants/{participant_id}",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        assert response.json() == {
            "success": True,
            "message": (
                "Participant profile deleted "
                "successfully"
            ),
        }

        missing_response = client.get(
            f"/participants/{participant_id}",
            headers=authorization_header(
                token
            ),
        )

        assert missing_response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_manager_can_read_participants():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.get(
            "/participants/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()


def test_manager_cannot_create_participant():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        target_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                manager.id,
                target_user.id,
            ]
        )

        response = client.post(
            (
                "/participants/users/"
                f"{target_user.id}"
            ),
            headers=authorization_header(
                token
            ),
            json={
                "chinese_name": "Forbidden",
                "gender": "male",
                "chinese_surname_id": None,
                "ethnicity_id": None,
                "ethnicity_other": None,
            },
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'participant.create' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
        )

        db.close()