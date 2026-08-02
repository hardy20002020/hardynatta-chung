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


def test_logout_revokes_user_sessions():
    email = (
        "logout-test-"
        f"{uuid4().hex}@example.com"
    )
    password = "MAJE-Test-Logout-2026!"

    db = SessionLocal()
    user_id = None

    try:
        # ==============================================
        # ARRANGE - CREATE ISOLATED TEST USER
        # ==============================================

        user = User(
            name="Logout Security Test",
            email=email,
            password=hash_password(password),
            role_id=2,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        user_id = user.id

        # ==============================================
        # LOGIN
        # ==============================================

        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == 200

        login_data = response.json()

        access_token = login_data["access_token"]
        refresh_token = login_data["refresh_token"]

        assert access_token
        assert refresh_token

        # ==============================================
        # VERIFY ACTIVE SESSION EXISTS
        # ==============================================

        db.expire_all()

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
        assert sessions[0].revoked_at is None
        assert sessions[0].revoke_reason is None

        # ==============================================
        # LOGOUT
        # ==============================================

        response = client.post(
            "/auth/logout",
            headers={
                "Authorization":
                    f"Bearer {access_token}",
            },
        )

        assert response.status_code == 200

        # ==============================================
        # VERIFY SESSION REVOKED
        # ==============================================

        db.expire_all()

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
        assert sessions[0].revoke_reason == "logout"

        # ==============================================
        # OLD REFRESH TOKEN MUST FAIL
        # ==============================================

        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": refresh_token,
            },
        )

        assert response.status_code == 401

        # ==============================================
        # OLD ACCESS TOKEN MUST FAIL
        # ==============================================

        response = client.get(
            "/auth/me",
            headers={
                "Authorization":
                    f"Bearer {access_token}",
            },
        )

        assert response.status_code == 401

        # ==============================================
        # VERIFY LOGOUT AUDIT EVENT
        # ==============================================

        audit_event = (
            db.execute(
                select(AuditLog)
                .where(
                    AuditLog.user_id
                    == user_id,
                    AuditLog.action
                    == "LOGOUT",
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
