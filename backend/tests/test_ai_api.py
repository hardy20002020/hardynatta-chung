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
from app.models.role import Role
from app.models.user import User
from app.models.user_session import UserSession


client = TestClient(app)


def authorization_header(token):
    return {
        "Authorization": f"Bearer {token}",
    }


def create_test_user(db, role_name: str):
    role = (
        db.query(Role)
        .filter(Role.name == role_name)
        .one()
    )

    email = (
        f"ai-{role_name}-test-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=f"AI {role_name.title()} Security Test",
        email=email,
        password=hash_password(
            "MAJE-AI-Test-2026!"
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


def cleanup_user(db, user_id: int):
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


def test_ai_generate_requires_authentication():
    response = client.post(
        "/ai/generate",
        json={
            "prompt": "Hello MAJE",
        },
    )

    assert response.status_code == 403


def test_manager_cannot_generate_ai():
    db = SessionLocal()
    user_id = None

    try:
        user, token = create_test_user(
            db,
            "manager",
        )

        user_id = user.id

        response = client.post(
            "/ai/generate",
            json={
                "prompt": "Hello MAJE",
            },
            headers=authorization_header(token),
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == "Permission 'ai.generate' required"
        )

    finally:
        if user_id is not None:
            cleanup_user(db, user_id)

        db.close()


def test_admin_can_generate_ai_and_audit_is_created():
    db = SessionLocal()
    user_id = None

    try:
        user, token = create_test_user(
            db,
            "admin",
        )

        user_id = user.id

        response = client.post(
            "/ai/generate",
            json={
                "prompt": "Hello MAJE",
            },
            headers=authorization_header(token),
        )

        assert response.status_code == 200

        data = response.json()

        assert data["success"] is True
        assert (
            data["message"]
            == "AI generation completed successfully"
        )
        assert (
            data["data"]["response"]
            == "AI service received prompt: Hello MAJE"
        )

        audit = (
            db.query(AuditLog)
            .filter(
                AuditLog.user_id == user.id,
                AuditLog.action == "AI_GENERATE",
                AuditLog.resource == "AI",
            )
            .order_by(
                AuditLog.id.desc()
            )
            .first()
        )

        assert audit is not None
        assert (
            audit.description
            == "AI generation request executed"
        )

    finally:
        if user_id is not None:
            cleanup_user(db, user_id)

        db.close()
