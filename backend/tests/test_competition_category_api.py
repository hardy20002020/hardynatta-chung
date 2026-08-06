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
from app.models.competition import Competition
from app.models.competition_category import (
    CompetitionCategory,
)
from app.models.role import Role
from app.models.user import User
from app.models.user_session import UserSession


client = TestClient(app)


def authorization_header(token):
    return {
        "Authorization": f"Bearer {token}",
    }


def create_test_user(
    db,
    role_name: str,
):
    role = (
        db.query(Role)
        .filter(Role.name == role_name)
        .one()
    )

    email = (
        "competition-category-api-test-"
        f"{role_name}-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=(
            "Competition Category API Test "
            f"{role_name.title()}"
        ),
        email=email,
        password=hash_password(
            "MAJE-Competition-Category-2026!"
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


def create_test_competition(
    db,
    code: str,
):
    competition = Competition(
        name="MAJE Competition Category Test",
        code=code,
        year=2026,
    )

    db.add(competition)
    db.commit()
    db.refresh(competition)

    return competition


def cleanup_test_data(
    db,
    user_ids,
    competition_codes,
):
    db.rollback()

    if competition_codes:
        competition_ids = [
            competition_id
            for (competition_id,) in (
                db.query(Competition.id)
                .filter(
                    Competition.code.in_(
                        competition_codes
                    )
                )
                .all()
            )
        ]

        if competition_ids:
            db.execute(
                delete(CompetitionCategory).where(
                    CompetitionCategory.competition_id.in_(
                        competition_ids
                    )
                )
            )

        db.execute(
            delete(Competition).where(
                Competition.code.in_(
                    competition_codes
                )
            )
        )

    if user_ids:
        db.execute(
            delete(UserSession).where(
                UserSession.user_id.in_(
                    user_ids
                )
            )
        )

        db.execute(
            delete(AuditLog).where(
                AuditLog.user_id.in_(
                    user_ids
                )
            )
        )

        db.execute(
            delete(User).where(
                User.id.in_(
                    user_ids
                )
            )
        )

    db.commit()


def test_admin_competition_category_crud():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-CATEGORY-CRUD-"
        f"{uuid4().hex[:12].upper()}"
    )

    competition_codes = [
        competition_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        competition = create_test_competition(
            db,
            competition_code,
        )

        headers = authorization_header(
            token
        )

        create_response = client.post(
            "/competition-categories/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "code": "MANDARIN",
                "name": "Mandarin Song",
                "description": (
                    "Mandarin singing category"
                ),
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert create_response.status_code == 201

        created = create_response.json()

        assert (
            created["competition_id"]
            == competition.id
        )
        assert created["code"] == "MANDARIN"
        assert created["name"] == "Mandarin Song"
        assert (
            created["description"]
            == "Mandarin singing category"
        )
        assert created["sort_order"] == 10
        assert created["is_active"] is True

        category_id = created["id"]

        list_response = client.get(
            "/competition-categories/",
            headers=headers,
        )

        assert list_response.status_code == 200

        assert any(
            category["id"] == category_id
            for category in list_response.json()
        )

        detail_response = client.get(
            (
                "/competition-categories/"
                f"{category_id}"
            ),
            headers=headers,
        )

        assert detail_response.status_code == 200

        assert (
            detail_response.json()["id"]
            == category_id
        )

        update_response = client.put(
            (
                "/competition-categories/"
                f"{category_id}"
            ),
            headers=headers,
            json={
                "code": "POP",
                "name": "Mandarin Pop",
                "description": (
                    "Mandarin pop song category"
                ),
                "sort_order": 20,
                "is_active": False,
            },
        )

        assert update_response.status_code == 200

        updated = update_response.json()

        assert updated["code"] == "POP"
        assert updated["name"] == "Mandarin Pop"
        assert (
            updated["description"]
            == "Mandarin pop song category"
        )
        assert updated["sort_order"] == 20
        assert updated["is_active"] is False

        delete_response = client.delete(
            (
                "/competition-categories/"
                f"{category_id}"
            ),
            headers=headers,
        )

        assert delete_response.status_code == 200

        assert delete_response.json() == {
            "success": True,
            "message": (
                "Competition category deleted "
                "successfully"
            ),
        }

        missing_response = client.get(
            (
                "/competition-categories/"
                f"{category_id}"
            ),
            headers=headers,
        )

        assert missing_response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_filter_categories_by_competition():
    db = SessionLocal()

    user_ids = []

    first_code = (
        "TEST-CATEGORY-FILTER-A-"
        f"{uuid4().hex[:10].upper()}"
    )

    second_code = (
        "TEST-CATEGORY-FILTER-B-"
        f"{uuid4().hex[:10].upper()}"
    )

    competition_codes = [
        first_code,
        second_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        first_competition = (
            create_test_competition(
                db,
                first_code,
            )
        )

        second_competition = (
            create_test_competition(
                db,
                second_code,
            )
        )

        first_category = CompetitionCategory(
            competition_id=first_competition.id,
            code="CAT-A",
            name="Category A",
            description="First category",
            sort_order=10,
        )

        second_category = CompetitionCategory(
            competition_id=second_competition.id,
            code="CAT-B",
            name="Category B",
            description="Second category",
            sort_order=20,
        )

        db.add_all(
            [
                first_category,
                second_category,
            ]
        )

        db.commit()
        db.refresh(first_category)
        db.refresh(second_category)

        response = client.get(
            (
                "/competition-categories/"
                f"?competition_id={first_competition.id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        categories = response.json()

        assert len(categories) == 1

        assert (
            categories[0]["id"]
            == first_category.id
        )

        assert (
            categories[0]["competition_id"]
            == first_competition.id
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_category_sort_order():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-CATEGORY-SORT-"
        f"{uuid4().hex[:12].upper()}"
    )

    competition_codes = [
        competition_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        competition = create_test_competition(
            db,
            competition_code,
        )

        categories = [
            CompetitionCategory(
                competition_id=competition.id,
                code="THIRD",
                name="Third",
                sort_order=30,
            ),
            CompetitionCategory(
                competition_id=competition.id,
                code="FIRST",
                name="First",
                sort_order=10,
            ),
            CompetitionCategory(
                competition_id=competition.id,
                code="SECOND",
                name="Second",
                sort_order=20,
            ),
        ]

        db.add_all(categories)
        db.commit()

        response = client.get(
            (
                "/competition-categories/"
                f"?competition_id={competition.id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        result = response.json()

        assert len(result) == 3

        assert [
            category["code"]
            for category in result
        ] == [
            "FIRST",
            "SECOND",
            "THIRD",
        ]

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_duplicate_category_code_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-CATEGORY-DUP-"
        f"{uuid4().hex[:12].upper()}"
    )

    competition_codes = [
        competition_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        competition = create_test_competition(
            db,
            competition_code,
        )

        headers = authorization_header(
            token
        )

        first_response = client.post(
            "/competition-categories/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "code": "SOLO",
                "name": "Solo",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert first_response.status_code == 201

        duplicate_response = client.post(
            "/competition-categories/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "code": "SOLO",
                "name": "Duplicate Solo",
                "description": None,
                "sort_order": 20,
                "is_active": True,
            },
        )

        assert duplicate_response.status_code == 409

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_same_category_code_allowed_in_different_competitions():
    db = SessionLocal()

    user_ids = []

    first_code = (
        "TEST-CATEGORY-SAME-A-"
        f"{uuid4().hex[:10].upper()}"
    )

    second_code = (
        "TEST-CATEGORY-SAME-B-"
        f"{uuid4().hex[:10].upper()}"
    )

    competition_codes = [
        first_code,
        second_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        first_competition = (
            create_test_competition(
                db,
                first_code,
            )
        )

        second_competition = (
            create_test_competition(
                db,
                second_code,
            )
        )

        headers = authorization_header(
            token
        )

        first_response = client.post(
            "/competition-categories/",
            headers=headers,
            json={
                "competition_id": (
                    first_competition.id
                ),
                "code": "SOLO",
                "name": "Solo",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert first_response.status_code == 201

        second_response = client.post(
            "/competition-categories/",
            headers=headers,
            json={
                "competition_id": (
                    second_competition.id
                ),
                "code": "SOLO",
                "name": "Solo",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert second_response.status_code == 201

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_duplicate_category_code_on_update_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-CATEGORY-UPDATE-DUP-"
        f"{uuid4().hex[:10].upper()}"
    )

    competition_codes = [
        competition_code,
    ]

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        competition = create_test_competition(
            db,
            competition_code,
        )

        first_category = CompetitionCategory(
            competition_id=competition.id,
            code="FIRST",
            name="First Category",
            sort_order=10,
        )

        second_category = CompetitionCategory(
            competition_id=competition.id,
            code="SECOND",
            name="Second Category",
            sort_order=20,
        )

        db.add_all(
            [
                first_category,
                second_category,
            ]
        )

        db.commit()
        db.refresh(first_category)
        db.refresh(second_category)

        response = client.put(
            (
                "/competition-categories/"
                f"{second_category.id}"
            ),
            headers=authorization_header(
                token
            ),
            json={
                "code": "FIRST",
                "name": "Duplicate",
                "description": None,
                "sort_order": 30,
                "is_active": True,
            },
        )

        assert response.status_code == 409

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_create_category_for_missing_competition_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.post(
            "/competition-categories/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": 2147483647,
                "code": "MISSING",
                "name": "Missing Competition",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_filter_missing_competition_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.get(
            (
                "/competition-categories/"
                "?competition_id=2147483647"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_competition_category_not_found_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.get(
            "/competition-categories/2147483647",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_update_missing_category_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.put(
            "/competition-categories/2147483647",
            headers=authorization_header(
                token
            ),
            json={
                "code": "MISSING",
                "name": "Missing Category",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_delete_missing_category_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.delete(
            "/competition-categories/2147483647",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_can_read_competition_categories():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.get(
            "/competition-categories/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_create_competition_category():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.post(
            "/competition-categories/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": 2147483647,
                "code": "FORBIDDEN",
                "name": "Forbidden",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_category.create' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_update_competition_category():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.put(
            "/competition-categories/2147483647",
            headers=authorization_header(
                token
            ),
            json={
                "code": "FORBIDDEN",
                "name": "Forbidden",
                "description": None,
                "sort_order": 10,
                "is_active": True,
            },
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_category.update' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_delete_competition_category():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.delete(
            "/competition-categories/2147483647",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_category.delete' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_user_cannot_read_competition_categories():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        user_ids.append(user.id)

        response = client.get(
            "/competition-categories/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_category.read' required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()