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


def test_refresh_token_reuse_revokes_family():
    email = (
        "refresh-test-"
        f"{uuid4().hex}@example.com"
    )
    password = "MAJE-Test-Refresh-2026!"

    db = SessionLocal()
    user_id = None

    try:
        # ==============================================
        # ARRANGE - CREATE ISOLATED TEST USER
        # ==============================================

        user = User(
            name="Refresh Token Security Test",
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
        # LOGIN - TOKEN A
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

        assert login_data["access_token"]
        assert login_data["refresh_token"]

        refresh_a = login_data["refresh_token"]

        # ==============================================
        # ROTATE TOKEN A -> TOKEN B
        # ==============================================

        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": refresh_a,
            },
        )

        assert response.status_code == 200

        refresh_data = response.json()

        assert refresh_data["access_token"]
        assert refresh_data["refresh_token"]

        refresh_b = refresh_data["refresh_token"]

        assert refresh_b != refresh_a

        # ==============================================
        # REUSE TOKEN A
        # ==============================================

        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": refresh_a,
            },
        )

        assert response.status_code == 401

        assert (
            response.json()["message"]
            == (
                "Refresh token reuse detected; "
                "session revoked"
            )
        )

        # ==============================================
        # TOKEN B MUST NOW BE INVALID
        # ==============================================

        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": refresh_b,
            },
        )

        assert response.status_code == 401

        # ==============================================
        # VERIFY DATABASE FAMILY STATE
        # ==============================================

        db.expire_all()

        sessions = (
            db.execute(
                select(UserSession)
                .where(
                    UserSession.user_id
                    == user_id
                )
                .order_by(UserSession.id)
            )
            .scalars()
            .all()
        )

        assert len(sessions) == 2

        families = {
            session.token_family
            for session in sessions
        }

        assert len(families) == 1

        for session in sessions:
            assert session.revoked_at is not None
            assert (
                session.revoke_reason
                == "reuse_detected"
            )

        # ==============================================
        # VERIFY SECURITY AUDIT EVENT
        # ==============================================

        audit_event = (
            db.execute(
                select(AuditLog)
                .where(
                    AuditLog.user_id
                    == user_id,
                    AuditLog.action
                    == "REFRESH_TOKEN_REUSE",
                )
            )
            .scalars()
            .first()
        )

        assert audit_event is not None

    finally:
        # ==============================================
        # CLEANUP TEST DATA
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
