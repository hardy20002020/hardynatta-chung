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


def test_user_without_permission_cannot_access_dashboard():
    email = (
        "rbac-no-permission-test-"
        f"{uuid4().hex}@example.com"
    )

    db = SessionLocal()
    user_id = None

    try:
        role = (
            db.query(Role)
            .filter(Role.name == "user")
            .one()
        )

        user = User(
            name="RBAC No Permission Security Test",
            email=email,
            password=hash_password(
                "MAJE-RBAC-User-2026!"
            ),
            role_id=role.id,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        user_id = user.id

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": "user",
                "role_id": role.id,
                "token_version": user.token_version,
            }
        )

        response = client.get(
            "/dashboard/",
            headers=authorization_header(token),
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == "Permission 'dashboard.read' required"
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


def test_forged_admin_claim_cannot_bypass_admin_role():
    email = (
        "rbac-forged-admin-test-"
        f"{uuid4().hex}@example.com"
    )

    db = SessionLocal()
    user_id = None

    try:
        role = (
            db.query(Role)
            .filter(Role.name == "user")
            .one()
        )

        user = User(
            name="RBAC Forged Admin Security Test",
            email=email,
            password=hash_password(
                "MAJE-RBAC-Forged-2026!"
            ),
            role_id=role.id,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        user_id = user.id

        # Deliberately forge privileged JWT claims.
        # Server-side RBAC must use the database role,
        # not trust these claims for authorization.
        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": "admin",
                "role_id": 1,
                "token_version": user.token_version,
            }
        )

        response = client.get(
            "/auth/admin-test",
            headers=authorization_header(token),
        )

        assert response.status_code == 403
        assert (
            response.json()["message"]
            == "Admin access required"
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


def test_manager_permission_allows_dashboard_access():
    email = (
        "rbac-manager-permission-test-"
        f"{uuid4().hex}@example.com"
    )

    db = SessionLocal()
    user_id = None

    try:
        role = (
            db.query(Role)
            .filter(Role.name == "manager")
            .one()
        )

        assert any(
            permission.name == "dashboard.read"
            for permission in role.permissions
        )

        user = User(
            name="RBAC Manager Security Test",
            email=email,
            password=hash_password(
                "MAJE-RBAC-Manager-2026!"
            ),
            role_id=role.id,
            is_active=True,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        user_id = user.id

        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": "manager",
                "role_id": role.id,
                "token_version": user.token_version,
            }
        )

        response = client.get(
            "/dashboard/",
            headers=authorization_header(token),
        )

        assert response.status_code == 200

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
