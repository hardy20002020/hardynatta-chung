from datetime import UTC, datetime, timedelta
from uuid import uuid4

from fastapi.testclient import TestClient
from jose import jwt
from sqlalchemy import delete

from app.core.config import settings
from app.core.security import (
    create_access_token,
    hash_password,
)
from app.db.session import SessionLocal
from app.main import app
from app.models.audit_log import AuditLog
from app.models.user import User
from app.models.user_session import UserSession


client = TestClient(app)


def authorization_header(token):
    return {
        "Authorization": f"Bearer {token}",
    }


def test_malformed_access_token_is_rejected():
    response = client.get(
        "/auth/me",
        headers=authorization_header(
            "definitely-invalid-access-token"
        ),
    )

    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "Invalid or expired token"
    )


def test_access_token_without_sub_is_rejected():
    token = create_access_token(
        {
            "token_version": 0,
        }
    )

    response = client.get(
        "/auth/me",
        headers=authorization_header(token),
    )

    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "Invalid token"
    )


def test_access_token_with_invalid_sub_is_rejected():
    token = create_access_token(
        {
            "sub": "not-a-user-id",
            "token_version": 0,
        }
    )

    response = client.get(
        "/auth/me",
        headers=authorization_header(token),
    )

    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "Invalid token"
    )


def test_access_token_without_token_version_is_rejected():
    email = (
        "access-token-version-test-"
        f"{uuid4().hex}@example.com"
    )

    db = SessionLocal()
    user_id = None

    try:
        user = User(
            name="Access Token Version Security Test",
            email=email,
            password=hash_password(
                "MAJE-Access-Token-2026!"
            ),
            role_id=2,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        user_id = user.id

        token = create_access_token(
            {
                "sub": str(user_id),
            }
        )

        response = client.get(
            "/auth/me",
            headers=authorization_header(token),
        )

        assert response.status_code == 401
        assert (
            response.json()["detail"]
            == "Token has been revoked"
        )

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


def test_revoked_access_token_version_is_rejected():
    email = (
        "revoked-access-token-test-"
        f"{uuid4().hex}@example.com"
    )

    db = SessionLocal()
    user_id = None

    try:
        user = User(
            name="Revoked Access Token Security Test",
            email=email,
            password=hash_password(
                "MAJE-Revoked-Token-2026!"
            ),
            role_id=2,
            is_active=True,
            token_version=1,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        user_id = user.id

        token = create_access_token(
            {
                "sub": str(user_id),
                "token_version": 0,
            }
        )

        response = client.get(
            "/auth/me",
            headers=authorization_header(token),
        )

        assert response.status_code == 401
        assert (
            response.json()["detail"]
            == "Token has been revoked"
        )

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


def test_expired_access_token_is_rejected():
    payload = {
        "sub": "1",
        "token_version": 0,
        "exp": (
            datetime.now(UTC)
            - timedelta(minutes=1)
        ),
    }

    token = jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    response = client.get(
        "/auth/me",
        headers=authorization_header(token),
    )

    assert response.status_code == 401
    assert (
        response.json()["detail"]
        == "Invalid or expired token"
    )
