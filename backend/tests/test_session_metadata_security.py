from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.core.security import (
    hash_password,
    hash_refresh_token,
)
from app.db.session import SessionLocal
from app.main import app
from app.models.audit_log import AuditLog
from app.models.user import User
from app.models.user_session import UserSession


client = TestClient(app)


def test_session_metadata_survives_refresh_rotation():
    email = (
        "session-metadata-test-"
        f"{uuid4().hex}@example.com"
    )

    db = SessionLocal()
    user_id = None

    try:
        user = User(
            name="Session Metadata Security Test",
            email=email,
            password=hash_password(
                "MAJE-Session-Metadata-2026!"
            ),
            role_id=2,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        user_id = user.id

        user_agent = (
            "MAJE-Security-Test/"
            f"{uuid4().hex}"
        )

        # ==============================================
        # LOGIN
        # ==============================================

        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password":
                    "MAJE-Session-Metadata-2026!",
            },
            headers={
                "user-agent": user_agent,
            },
        )

        assert response.status_code == 200

        login_data = response.json()

        refresh_a = login_data["refresh_token"]

        session_a = (
            db.execute(
                select(UserSession)
                .where(
                    UserSession.user_id == user_id,
                    UserSession.refresh_token_hash
                    == hash_refresh_token(refresh_a),
                )
            )
            .scalar_one()
        )

        assert session_a.user_agent == user_agent
        assert session_a.ip_address is not None
        assert len(session_a.ip_address) <= 45

        original_ip = session_a.ip_address
        original_family = session_a.token_family

        # ==============================================
        # REFRESH / ROTATION
        # ==============================================

        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": refresh_a,
            },
        )

        assert response.status_code == 200

        refresh_data = response.json()
        refresh_b = refresh_data["refresh_token"]

        db.expire_all()

        session_b = (
            db.execute(
                select(UserSession)
                .where(
                    UserSession.user_id == user_id,
                    UserSession.refresh_token_hash
                    == hash_refresh_token(refresh_b),
                )
            )
            .scalar_one()
        )

        assert session_b.token_family == original_family
        assert session_b.user_agent == user_agent
        assert session_b.ip_address == original_ip

        db.expire_all()

        old_session = (
            db.execute(
                select(UserSession)
                .where(
                    UserSession.user_id == user_id,
                    UserSession.refresh_token_hash
                    == hash_refresh_token(refresh_a),
                )
            )
            .scalar_one()
        )

        assert old_session.revoked_at is not None
        assert old_session.revoke_reason == "rotated"
        assert old_session.last_used_at is not None

    finally:
        if user_id is not None:
            db.rollback()

            db.execute(
                delete(UserSession).where(
                    UserSession.user_id == user_id
                )
            )

            db.execute(
                delete(AuditLog).where(
                    AuditLog.user_id == user_id
                )
            )

            db.execute(
                delete(User).where(
                    User.id == user_id
                )
            )

            db.commit()

        db.close()
