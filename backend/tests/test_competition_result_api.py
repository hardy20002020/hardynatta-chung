from uuid import uuid4

from fastapi.testclient import TestClient

from app.core.security import (
    create_access_token,
    hash_password,
)
from app.db.session import SessionLocal
from app.main import app

from app.models.role import Role
from app.models.user import User

from tests.test_competition_result_finalization_service import (
    create_finalization_context,
    cleanup_finalization_context,
)


client = TestClient(app)


# ==========================================================
# AUTHORIZATION
# ==========================================================

def authorization_header(
    token: str,
):
    return {
        "Authorization": f"Bearer {token}",
    }


# ==========================================================
# USER
# ==========================================================

def create_api_user(
    db,
    role_name: str,
):
    role = (
        db.query(Role)
        .filter(
            Role.name == role_name
        )
        .one()
    )

    user = User(
        name=(
            "Competition Result API Test "
            f"{role_name.title()}"
        ),
        email=(
            "competition-result-api-test-"
            f"{role_name}-"
            f"{uuid4().hex}@example.com"
        ),
        password=hash_password(
            "MAJE-Result-API-2026!"
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


# ==========================================================
# TOKEN FOR EXISTING USER
# ==========================================================

def create_token_for_user(
    user,
):
    return create_access_token(
        {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role_ref.name,
            "role_id": user.role_id,
            "token_version": user.token_version,
        }
    )


# ==========================================================
# FINALIZE + READ
# ==========================================================

def test_admin_can_finalize_and_read_results():
    db = SessionLocal()
    context = None

    try:
        context = create_finalization_context(
            db,
            complete=True,
        )

        admin = context["finalizer"]

        token = create_token_for_user(
            admin
        )

        round_id = context["round"].id

        response = client.post(
            (
                "/competition-results/"
                f"rounds/{round_id}/finalize"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        data = response.json()

        assert (
            data["competition_round_id"]
            == round_id
        )
        assert data["status"] == "finalized"
        assert data["total_results"] == 3
        assert (
            data["finalized_by_user_id"]
            == admin.id
        )

        results = data["results"]

        assert len(results) == 3

        assert results[0]["rank"] == 1
        assert results[1]["rank"] == 1
        assert results[2]["rank"] == 3

        read_response = client.get(
            "/competition-results/",
            params={
                "competition_round_id": (
                    round_id
                ),
            },
            headers=authorization_header(
                token
            ),
        )

        assert read_response.status_code == 200

        persisted = read_response.json()

        assert len(persisted) == 3

        assert [
            result["rank"]
            for result in persisted
        ] == [
            1,
            1,
            3,
        ]

        detail_response = client.get(
            (
                "/competition-results/"
                f"{persisted[0]['id']}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert detail_response.status_code == 200

        assert (
            detail_response.json()["id"]
            == persisted[0]["id"]
        )

    finally:
        if context is not None:
            cleanup_finalization_context(
                db,
                context,
            )

        db.close()


# ==========================================================
# SECOND FINALIZATION
# ==========================================================

def test_second_finalization_returns_conflict():
    db = SessionLocal()
    context = None

    try:
        context = create_finalization_context(
            db,
            complete=True,
        )

        admin = context["finalizer"]

        token = create_token_for_user(
            admin
        )

        round_id = context["round"].id

        first_response = client.post(
            (
                "/competition-results/"
                f"rounds/{round_id}/finalize"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert first_response.status_code == 200

        second_response = client.post(
            (
                "/competition-results/"
                f"rounds/{round_id}/finalize"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert second_response.status_code == 409

        assert (
            second_response.json()["message"]
            == (
                "Competition round results "
                "already finalized"
            )
        )

    finally:
        if context is not None:
            cleanup_finalization_context(
                db,
                context,
            )

        db.close()


# ==========================================================
# INCOMPLETE SCORING
# ==========================================================

def test_incomplete_round_cannot_be_finalized():
    db = SessionLocal()
    context = None

    try:
        context = create_finalization_context(
            db,
            complete=False,
        )

        admin = context["finalizer"]

        token = create_token_for_user(
            admin
        )

        response = client.post(
            (
                "/competition-results/"
                f"rounds/{context['round'].id}/"
                "finalize"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 409

        assert (
            response.json()["message"]
            == (
                "Competition round scoring "
                "is incomplete"
            )
        )

    finally:
        if context is not None:
            cleanup_finalization_context(
                db,
                context,
            )

        db.close()


# ==========================================================
# MANAGER RBAC
# ==========================================================

def test_manager_can_read_but_cannot_finalize():
    db = SessionLocal()
    context = None
    manager = None

    try:
        context = create_finalization_context(
            db,
            complete=True,
        )

        admin = context["finalizer"]

        admin_token = create_token_for_user(
            admin
        )

        round_id = context["round"].id

        finalize_response = client.post(
            (
                "/competition-results/"
                f"rounds/{round_id}/finalize"
            ),
            headers=authorization_header(
                admin_token
            ),
        )

        assert finalize_response.status_code == 200

        manager, manager_token = create_api_user(
            db,
            "manager",
        )

        read_response = client.get(
            "/competition-results/",
            params={
                "competition_round_id": (
                    round_id
                ),
            },
            headers=authorization_header(
                manager_token
            ),
        )

        assert read_response.status_code == 200
        assert len(read_response.json()) == 3

        finalize_response = client.post(
            (
                "/competition-results/"
                f"rounds/{round_id}/finalize"
            ),
            headers=authorization_header(
                manager_token
            ),
        )

        assert finalize_response.status_code == 403

        assert (
            finalize_response.json()["message"]
            == (
                "Permission "
                "'competition_result.finalize' "
                "required"
            )
        )

    finally:
        if manager is not None:
            db.delete(manager)
            db.commit()

        if context is not None:
            cleanup_finalization_context(
                db,
                context,
            )

        db.close()


# ==========================================================
# USER RBAC
# ==========================================================

def test_user_cannot_read_results():
    db = SessionLocal()
    context = None
    user = None

    try:
        context = create_finalization_context(
            db,
            complete=True,
        )

        user, token = create_api_user(
            db,
            "user",
        )

        response = client.get(
            "/competition-results/",
            params={
                "competition_round_id": (
                    context["round"].id
                ),
            },
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_result.read' "
                "required"
            )
        )

    finally:
        if user is not None:
            db.delete(user)
            db.commit()

        if context is not None:
            cleanup_finalization_context(
                db,
                context,
            )

        db.close()


# ==========================================================
# NOT FOUND
# ==========================================================

def test_result_not_found_returns_404():
    db = SessionLocal()
    context = None

    try:
        context = create_finalization_context(
            db,
            complete=True,
        )

        admin = context["finalizer"]

        token = create_token_for_user(
            admin
        )

        response = client.get(
            "/competition-results/2147483647",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

        assert (
            response.json()["message"]
            == "Competition result not found"
        )

    finally:
        if context is not None:
            cleanup_finalization_context(
                db,
                context,
            )

        db.close()
