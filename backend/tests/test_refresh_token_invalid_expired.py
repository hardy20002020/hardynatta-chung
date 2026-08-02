from datetime import UTC, datetime, timedelta
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


def test_invalid_refresh_token_is_rejected():
    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token":
                "definitely-invalid-refresh-token",
        },
    )

    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "Invalid refresh token"
    )


def test_expired_refresh_token_is_rejected():
    email = (
        "expired-refresh-test-"
        f"{uuid4().hex}@example.com"
    )
    password = "MAJE-Expired-Refresh-2026!"

    db = SessionLocal()
    user_id = None

    try:
        # ==============================================
        # ARRANGE - CREATE ISOLATED USER
        # ==============================================

        user = User(
            name="Expired Refresh Security Test",
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
        # LOGIN TO CREATE REAL REFRESH SESSION
        # ==============================================

        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == 200

        refresh_token = response.json()[
            "refresh_token"
        ]

        assert refresh_token

        # ==============================================
        # FORCE SESSION TO BE EXPIRED
        # ==============================================

        session = (
            db.execute(
                select(UserSession)
                .where(
                    UserSession.user_id
                    == user_id,
                    UserSession.refresh_token_hash
                    == hash_refresh_token(
                        refresh_token
                    ),
                )
            )
            .scalars()
            .one()
        )

        session.expires_at = (
            datetime.now(UTC)
            .replace(tzinfo=None)
            - timedelta(minutes=1)
        )

        db.commit()

        # ==============================================
        # EXPIRED TOKEN MUST FAIL
        # ==============================================

        response = client.post(
            "/auth/refresh",
            json={
                "refresh_token": refresh_token,
            },
        )

        assert response.status_code == 401
        assert (
            response.json()["detail"]
            == "Refresh token has expired"
        )

        # ==============================================
        # VERIFY EXPIRED REVOCATION STATE
        # ==============================================

        db.expire_all()

        expired_session = (
            db.execute(
                select(UserSession)
                .where(
                    UserSession.user_id
                    == user_id,
                    UserSession.refresh_token_hash
                    == hash_refresh_token(
                        refresh_token
                    ),
                )
            )
            .scalars()
            .one()
        )

        assert expired_session.revoked_at is not None
        assert (
            expired_session.revoke_reason
            == "expired"
        )

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
