from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy import delete, select

from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.main import app
from app.models.audit_log import AuditLog
from app.models.user import User
from app.models.user_session import UserSession


client = TestClient(app)


def test_account_lockout_and_expiry_reset():
    email = (
        "lockout-security-test-"
        f"{uuid4().hex}@example.com"
    )

    password = "MAJE-Lockout-Test-2026!"
    wrong_password = "Wrong-Password-2026!"

    db = SessionLocal()
    user_id = None

    try:
        # ==============================================
        # CREATE ISOLATED TEST USER
        # ==============================================

        user = User(
            name="Account Lockout Security Test",
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
        # REPEATED FAILED LOGIN ATTEMPTS
        # ==============================================

        for _ in range(
            settings.MAX_FAILED_LOGIN_ATTEMPTS
        ):
            response = client.post(
                "/auth/login",
                json={
                    "email": email,
                    "password": wrong_password,
                },
            )

            assert response.status_code == 401
            assert (
                response.json()["detail"]
                == "Invalid email or password"
            )

        # ==============================================
        # VERIFY DATABASE LOCKOUT STATE
        # ==============================================

        db.expire_all()

        locked_user = (
            db.execute(
                select(User).where(
                    User.id == user_id
                )
            )
            .scalars()
            .one()
        )

        assert (
            locked_user.failed_login_attempts
            == settings.MAX_FAILED_LOGIN_ATTEMPTS
        )

        assert locked_user.locked_until is not None

        # ==============================================
        # ISOLATE LOCKOUT CHECK FROM RATE LIMIT
        # ==============================================

        limiter.reset()

        # Correct password must still be rejected
        # while account lockout is active.
        response = client.post(
            "/auth/login",
            json={
                "email": email,
                "password": password,
            },
        )

        assert response.status_code == 423
        assert (
            response.json()["detail"]
            == "Account is temporarily locked"
        )

        # ==============================================
        # SIMULATE LOCKOUT EXPIRY
        # ==============================================

        locked_user.locked_until = (
            datetime.now(UTC)
            .replace(tzinfo=None)
            - timedelta(seconds=1)
        )

        db.commit()

        limiter.reset()

        # ==============================================
        # LOGIN AFTER LOCKOUT EXPIRY
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

        # ==============================================
        # VERIFY LOCKOUT STATE RESET
        # ==============================================

        db.expire_all()

        recovered_user = (
            db.execute(
                select(User).where(
                    User.id == user_id
                )
            )
            .scalars()
            .one()
        )

        assert recovered_user.failed_login_attempts == 0
        assert recovered_user.locked_until is None

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
