from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.core.security import hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.audit_log import AuditLog
from app.models.user import User
from app.models.user_session import UserSession


client = TestClient(app)


def test_password_change_revokes_existing_tokens():
    email = (
        "password-change-test-"
        f"{uuid4().hex}@example.com"
    )

    old_password = "MAJE-Old-Password-2026!"
    new_password = "MAJE-New-Password-2026!"

    db = SessionLocal()
    user_id = None

    try:
        # ==============================================
        # ARRANGE - CREATE ISOLATED TEST USER
        # ==============================================

        user = User(
            name="Password Change Security Test",
            email=email,
            password=hash_password(old_password),
            role_id=2,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        user_id = user.id
        original_token_version = user.token_version

        # ==============================================
        # LOGIN WITH OLD PASSWORD
        # ==============================================

        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": old_password,
            },
        )

        assert response.status_code == 200

        login_data = response.json()

        old_access_token = login_data["access_token"]
        old_refresh_token = login_data["refresh_token"]

        assert old_access_token
        assert old_refresh_token

        # ==============================================
        # CHANGE PASSWORD
        # ==============================================

        response = client.post(
            "/auth/change-password",
            headers={
                "Authorization":
                    f"Bearer {old_access_token}",
            },
            json={
                "current_password": old_password,
                "new_password": new_password,
            },
        )

        assert response.status_code == 200

        assert response.json()["success"] is True
        assert (
            response.json()["message"]
            == "Password changed successfully"
        )

        # ==============================================
        # VERIFY TOKEN VERSION INCREMENTED
        # ==============================================

        db.expire_all()

        changed_user = (
            db.execute(
                select(User).where(
                    User.id == user_id
                )
            )
            .scalars()
            .one()
        )

        assert (
            changed_user.token_version
            == original_token_version + 1
        )

        # ==============================================
        # VERIFY EXISTING SESSION REVOKED
        # ==============================================

        sessions = (
            db.execute(
                select(UserSession)
                .where(
                    UserSession.user_id
                    == user_id
                )
            )
            .scalars()
            .all()
        )

        assert len(sessions) == 1
        assert sessions[0].revoked_at is not None
        assert (
            sessions[0].revoke_reason
            == "password_change"
        )

        # ==============================================
        # OLD ACCESS TOKEN MUST FAIL
        # ==============================================

        response = client.get(
            "/auth/me",
            headers={
                "Authorization":
                    f"Bearer {old_access_token}",
            },
        )

        assert response.status_code == 401

        # ==============================================
        # OLD REFRESH TOKEN MUST FAIL
        # ==============================================

        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": old_refresh_token,
            },
        )

        assert response.status_code == 401

        # ==============================================
        # OLD PASSWORD MUST FAIL
        # ==============================================

        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": old_password,
            },
        )

        assert response.status_code == 401

        # ==============================================
        # NEW PASSWORD MUST LOGIN SUCCESSFULLY
        # ==============================================

        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": new_password,
            },
        )

        assert response.status_code == 200

        new_login_data = response.json()

        assert new_login_data["access_token"]
        assert new_login_data["refresh_token"]

        # ==============================================
        # VERIFY PASSWORD CHANGE AUDIT EVENT
        # ==============================================

        audit_event = (
            db.execute(
                select(AuditLog)
                .where(
                    AuditLog.user_id
                    == user_id,
                    AuditLog.action
                    == "PASSWORD_CHANGE",
                )
            )
            .scalars()
            .first()
        )

        assert audit_event is not None

    finally:
        # ==============================================
        # CLEANUP
        # ==============================================

        if user_id is not None:
            db.rollback()

            db.execute(
                delete(UserSession).where(
                    UserSession.user_id
                    == user_id
                )
            )

            db.execute(
                delete(AuditLog).where(
                    AuditLog.user_id
                    == user_id
                )
            )

            db.execute(
                delete(User).where(
                    User.id
                    == user_id
                )
            )

            db.commit()

        db.close()
