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


def test_inactive_user_cannot_login_or_refresh():
    email = (
        "inactive-security-test-"
        f"{uuid4().hex}@example.com"
    )
    password = "MAJE-Inactive-Test-2026!"

    db = SessionLocal()
    user_id = None

    try:
        # ==============================================
        # CREATE ACTIVE TEST USER
        # ==============================================

        user = User(
            name="Inactive Account Security Test",
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
        # LOGIN WHILE ACTIVE
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
        # DEACTIVATE ACCOUNT
        # ==============================================

        user.is_active = False
        db.commit()

        # ==============================================
        # NEW LOGIN MUST FAIL
        # ==============================================

        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "Account is inactive"
        )

        # ==============================================
        # EXISTING REFRESH TOKEN MUST FAIL
        # ==============================================

        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": refresh_token,
            },
        )

        assert response.status_code == 403
        assert (
            response.json()["detail"]
            == "Account is inactive"
        )

        # ==============================================
        # REFRESH SESSION MUST BE REVOKED
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

        # ==============================================
        # EXISTING ACCESS TOKEN MUST FAIL
        # ==============================================

        response = client.get(
            "/auth/me",
            headers={
                "Authorization":
                    f"Bearer {access_token}",
            },
        )

        assert response.status_code in (401, 403)

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
