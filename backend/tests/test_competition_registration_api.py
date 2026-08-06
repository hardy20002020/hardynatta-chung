from datetime import date
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
from app.models.competition_group import CompetitionGroup
from app.models.competition_registration import (
    CompetitionRegistration,
)
from app.models.participant import Participant
from app.models.role import Role
from app.models.user import User
from app.models.user_session import UserSession


client = TestClient(app)


# ==========================================================
# AUTHORIZATION
# ==========================================================

def authorization_header(token):
    return {
        "Authorization": f"Bearer {token}",
    }


# ==========================================================
# TEST DATA HELPERS
# ==========================================================

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
        "competition-registration-api-test-"
        f"{role_name}-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=(
            "Competition Registration API Test "
            f"{role_name.title()}"
        ),
        email=email,
        password=hash_password(
            "MAJE-Registration-2026!"
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
    age_reference_date: date | None = date(
        2026,
        1,
        1,
    ),
):
    competition = Competition(
        name="MAJE Registration Test Competition",
        code=code,
        year=2026,
        age_reference_date=age_reference_date,
    )

    db.add(competition)
    db.commit()
    db.refresh(competition)

    return competition


def create_test_group(
    db,
    competition_id: int,
    code: str,
    name: str,
    min_age: int | None = None,
    max_age: int | None = None,
):
    group = CompetitionGroup(
        competition_id=competition_id,
        code=code,
        name=name,
        min_age=min_age,
        max_age=max_age,
        sort_order=10,
        is_active=True,
    )

    db.add(group)
    db.commit()
    db.refresh(group)

    return group


def create_test_category(
    db,
    competition_id: int,
    code: str,
    name: str,
):
    category = CompetitionCategory(
        competition_id=competition_id,
        code=code,
        name=name,
        description=(
            "MAJE competition registration "
            "test category"
        ),
        sort_order=10,
        is_active=True,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    return category


def create_test_participant(
    db,
    user_id: int,
    date_of_birth: date,
):
    participant = Participant(
        user_id=user_id,
        chinese_name="测试参赛者",
        gender="male",
        date_of_birth=date_of_birth,
    )

    db.add(participant)
    db.commit()
    db.refresh(participant)

    return participant


# ==========================================================
# CLEANUP
# ==========================================================

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
                delete(
                    CompetitionRegistration
                ).where(
                    CompetitionRegistration
                    .competition_id.in_(
                        competition_ids
                    )
                )
            )

            db.execute(
                delete(
                    CompetitionCategory
                ).where(
                    CompetitionCategory
                    .competition_id.in_(
                        competition_ids
                    )
                )
            )

            db.execute(
                delete(
                    CompetitionGroup
                ).where(
                    CompetitionGroup
                    .competition_id.in_(
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
            delete(
                CompetitionRegistration
            ).where(
                CompetitionRegistration
                .participant_id.in_(
                    db.query(Participant.id)
                    .filter(
                        Participant.user_id.in_(
                            user_ids
                        )
                    )
                )
            )
        )

        db.execute(
            delete(Participant).where(
                Participant.user_id.in_(
                    user_ids
                )
            )
        )

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


# ==========================================================
# ADMIN CRUD
# ==========================================================

def test_admin_competition_registration_crud():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-CRUD-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
        )

        first_group = create_test_group(
            db,
            competition.id,
            "REMAJA",
            "Remaja",
            min_age=13,
            max_age=17,
        )

        second_group = create_test_group(
            db,
            competition.id,
            "UMUM",
            "Umum",
            min_age=13,
            max_age=25,
        )

        first_category = create_test_category(
            db,
            competition.id,
            "MANDARIN",
            "Mandarin",
        )

        second_category = create_test_category(
            db,
            competition.id,
            "HOKKIEN",
            "Hokkien",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2010,
                1,
                1,
            ),
        )

        headers = authorization_header(
            token
        )

        registration_number = (
            "REG-"
            f"{uuid4().hex[:12].upper()}"
        )

        create_response = client.post(
            "/competition-registrations/",
            headers=headers,
            json={
                "competition_id": (
                    competition.id
                ),
                "competition_group_id": (
                    first_group.id
                ),
                "competition_category_id": (
                    first_category.id
                ),
                "participant_id": (
                    participant.id
                ),
                "registration_number": (
                    registration_number
                ),
            },
        )

        assert create_response.status_code == 201

        created = create_response.json()

        assert (
            created["competition_id"]
            == competition.id
        )

        assert (
            created["competition_group_id"]
            == first_group.id
        )

        assert (
            created["competition_category_id"]
            == first_category.id
        )

        assert (
            created["participant_id"]
            == participant.id
        )

        assert (
            created["registration_number"]
            == registration_number
        )

        assert (
            created["status"]
            == "registered"
        )

        registration_id = created["id"]

        list_response = client.get(
            "/competition-registrations/",
            headers=headers,
        )

        assert list_response.status_code == 200

        assert any(
            registration["id"]
            == registration_id
            for registration
            in list_response.json()
        )

        detail_response = client.get(
            (
                "/competition-registrations/"
                f"{registration_id}"
            ),
            headers=headers,
        )

        assert detail_response.status_code == 200

        assert (
            detail_response.json()["id"]
            == registration_id
        )

        updated_number = (
            "REG-UPD-"
            f"{uuid4().hex[:10].upper()}"
        )

        update_response = client.put(
            (
                "/competition-registrations/"
                f"{registration_id}"
            ),
            headers=headers,
            json={
                "competition_group_id": (
                    second_group.id
                ),
                "competition_category_id": (
                    second_category.id
                ),
                "registration_number": (
                    updated_number
                ),
                "status": "confirmed",
            },
        )

        assert update_response.status_code == 200

        updated = update_response.json()

        assert (
            updated["competition_group_id"]
            == second_group.id
        )

        assert (
            updated["competition_category_id"]
            == second_category.id
        )

        assert (
            updated["registration_number"]
            == updated_number
        )

        assert (
            updated["status"]
            == "confirmed"
        )

        delete_response = client.delete(
            (
                "/competition-registrations/"
                f"{registration_id}"
            ),
            headers=headers,
        )

        assert delete_response.status_code == 200

        assert delete_response.json() == {
            "success": True,
            "message": (
                "Competition registration "
                "deleted successfully"
            ),
        }

        missing_response = client.get(
            (
                "/competition-registrations/"
                f"{registration_id}"
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


# ==========================================================
# FILTER
# ==========================================================

def test_filter_registrations_by_competition():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-FILTER-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
        )

        group = create_test_group(
            db,
            competition.id,
            "FILTER",
            "Filter Group",
            min_age=10,
            max_age=30,
        )

        category = create_test_category(
            db,
            competition.id,
            "FILTER-CAT",
            "Filter Category",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2005,
                1,
                1,
            ),
        )

        registration = CompetitionRegistration(
            competition_id=competition.id,
            competition_group_id=group.id,
            competition_category_id=category.id,
            participant_id=participant.id,
            registration_number=(
                "FILTER-"
                f"{uuid4().hex[:10].upper()}"
            ),
            status="registered",
        )

        db.add(registration)
        db.commit()
        db.refresh(registration)

        response = client.get(
            (
                "/competition-registrations/"
                f"?competition_id={competition.id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        registrations = response.json()

        assert any(
            item["id"] == registration.id
            for item in registrations
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_filter_registrations_by_participant():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-PART-FILTER-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
        )

        group = create_test_group(
            db,
            competition.id,
            "PF",
            "Participant Filter",
            min_age=10,
            max_age=30,
        )

        category = create_test_category(
            db,
            competition.id,
            "PF-CAT",
            "Participant Filter Category",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2005,
                1,
                1,
            ),
        )

        registration = CompetitionRegistration(
            competition_id=competition.id,
            competition_group_id=group.id,
            competition_category_id=category.id,
            participant_id=participant.id,
            registration_number=(
                "PF-"
                f"{uuid4().hex[:10].upper()}"
            ),
            status="registered",
        )

        db.add(registration)
        db.commit()
        db.refresh(registration)

        response = client.get(
            (
                "/competition-registrations/"
                f"?participant_id={participant.id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        registrations = response.json()

        assert len(registrations) == 1

        assert (
            registrations[0]["id"]
            == registration.id
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_filter_registrations_by_category():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-CAT-FILTER-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
        )

        group = create_test_group(
            db,
            competition.id,
            "CF",
            "Category Filter Group",
            min_age=10,
            max_age=30,
        )

        category = create_test_category(
            db,
            competition.id,
            "CF-CAT",
            "Category Filter",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2005,
                1,
                1,
            ),
        )

        registration = CompetitionRegistration(
            competition_id=competition.id,
            competition_group_id=group.id,
            competition_category_id=category.id,
            participant_id=participant.id,
            registration_number=(
                "CF-"
                f"{uuid4().hex[:10].upper()}"
            ),
            status="registered",
        )

        db.add(registration)
        db.commit()
        db.refresh(registration)

        response = client.get(
            (
                "/competition-registrations/"
                "?competition_category_id="
                f"{category.id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        registrations = response.json()

        assert len(registrations) == 1

        assert (
            registrations[0]["id"]
            == registration.id
        )

        assert (
            registrations[0][
                "competition_category_id"
            ]
            == category.id
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


# ==========================================================
# DUPLICATE VALIDATION
# ==========================================================

def test_duplicate_participant_registration_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-DUP-PART-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
        )

        group = create_test_group(
            db,
            competition.id,
            "DP",
            "Duplicate Participant",
            min_age=10,
            max_age=30,
        )

        category = create_test_category(
            db,
            competition.id,
            "DUP-PART",
            "Duplicate Participant Category",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2005,
                1,
                1,
            ),
        )

        headers = authorization_header(
            token
        )

        first_response = client.post(
            "/competition-registrations/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "competition_group_id": group.id,
                "competition_category_id": category.id,
                "participant_id": participant.id,
                "registration_number": (
                    "DUP-A-"
                    f"{uuid4().hex[:8].upper()}"
                ),
            },
        )

        assert first_response.status_code == 201

        duplicate_response = client.post(
            "/competition-registrations/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "competition_group_id": group.id,
                "competition_category_id": category.id,
                "participant_id": participant.id,
                "registration_number": (
                    "DUP-B-"
                    f"{uuid4().hex[:8].upper()}"
                ),
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


def test_duplicate_registration_number_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-DUP-NUM-"
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

        first_user, _ = create_test_user(
            db,
            "user",
        )

        second_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                first_user.id,
                second_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
        )

        group = create_test_group(
            db,
            competition.id,
            "DN",
            "Duplicate Number",
            min_age=10,
            max_age=30,
        )

        category = create_test_category(
            db,
            competition.id,
            "DUP-NUM",
            "Duplicate Number Category",
        )

        first_participant = create_test_participant(
            db,
            first_user.id,
            date(
                2005,
                1,
                1,
            ),
        )

        second_participant = create_test_participant(
            db,
            second_user.id,
            date(
                2006,
                1,
                1,
            ),
        )

        headers = authorization_header(
            token
        )

        registration_number = (
            "SAME-"
            f"{uuid4().hex[:10].upper()}"
        )

        first_response = client.post(
            "/competition-registrations/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "competition_group_id": group.id,
                "competition_category_id": category.id,
                "participant_id": (
                    first_participant.id
                ),
                "registration_number": (
                    registration_number
                ),
            },
        )

        assert first_response.status_code == 201

        duplicate_response = client.post(
            "/competition-registrations/",
            headers=headers,
            json={
                "competition_id": competition.id,
                "competition_group_id": group.id,
                "competition_category_id": category.id,
                "participant_id": (
                    second_participant.id
                ),
                "registration_number": (
                    registration_number
                ),
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


# ==========================================================
# RELATION VALIDATION
# ==========================================================

def test_group_from_different_competition_is_rejected():
    db = SessionLocal()

    user_ids = []

    first_code = (
        "TEST-REG-GROUP-A-"
        f"{uuid4().hex[:10].upper()}"
    )

    second_code = (
        "TEST-REG-GROUP-B-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

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

        wrong_group = create_test_group(
            db,
            second_competition.id,
            "WRONG",
            "Wrong Competition Group",
            min_age=10,
            max_age=30,
        )

        category = create_test_category(
            db,
            first_competition.id,
            "RELATION",
            "Relation Validation Category",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2005,
                1,
                1,
            ),
        )

        response = client.post(
            "/competition-registrations/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": (
                    first_competition.id
                ),
                "competition_group_id": (
                    wrong_group.id
                ),
                "competition_category_id": (
                    category.id
                ),
                "participant_id": (
                    participant.id
                ),
                "registration_number": (
                    "WRONG-"
                    f"{uuid4().hex[:8].upper()}"
                ),
            },
        )

        assert response.status_code == 400

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_missing_competition_returns_404():
    db = SessionLocal()

    user_ids = []

    try:
        admin, token = create_test_user(
            db,
            "admin",
        )

        user_ids.append(admin.id)

        response = client.post(
            "/competition-registrations/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": 2147483647,
                "competition_group_id": 2147483647,
                "competition_category_id": 2147483647,
                "participant_id": 2147483647,
                "registration_number": "MISSING-COMP",
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


def test_registration_not_found_returns_404():
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
                "/competition-registrations/"
                "2147483647"
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


# ==========================================================
# AGE ELIGIBILITY
# ==========================================================

def test_participant_below_minimum_age_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-AGE-MIN-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
            age_reference_date=date(
                2026,
                1,
                1,
            ),
        )

        group = create_test_group(
            db,
            competition.id,
            "AGE13",
            "Age 13 Plus",
            min_age=13,
            max_age=17,
        )

        category = create_test_category(
            db,
            competition.id,
            "AGE-MIN",
            "Minimum Age Category",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2013,
                1,
                2,
            ),
        )

        response = client.post(
            "/competition-registrations/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": competition.id,
                "competition_group_id": group.id,
                "competition_category_id": category.id,
                "participant_id": participant.id,
                "registration_number": (
                    "AGE-MIN-"
                    f"{uuid4().hex[:8].upper()}"
                ),
            },
        )

        assert response.status_code == 400

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_participant_at_minimum_age_is_accepted():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-AGE-BOUND-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
            age_reference_date=date(
                2026,
                1,
                1,
            ),
        )

        group = create_test_group(
            db,
            competition.id,
            "AGE13",
            "Age 13 Plus",
            min_age=13,
            max_age=17,
        )

        category = create_test_category(
            db,
            competition.id,
            "AGE-BOUND",
            "Age Boundary Category",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2013,
                1,
                1,
            ),
        )

        response = client.post(
            "/competition-registrations/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": competition.id,
                "competition_group_id": group.id,
                "competition_category_id": category.id,
                "participant_id": participant.id,
                "registration_number": (
                    "AGE-BOUND-"
                    f"{uuid4().hex[:8].upper()}"
                ),
            },
        )

        assert response.status_code == 201

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_participant_above_maximum_age_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-AGE-MAX-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
            age_reference_date=date(
                2026,
                1,
                1,
            ),
        )

        group = create_test_group(
            db,
            competition.id,
            "MAX17",
            "Maximum Age 17",
            min_age=13,
            max_age=17,
        )

        category = create_test_category(
            db,
            competition.id,
            "AGE-MAX",
            "Maximum Age Category",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2008,
                1,
                1,
            ),
        )

        response = client.post(
            "/competition-registrations/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": competition.id,
                "competition_group_id": group.id,
                "competition_category_id": category.id,
                "participant_id": participant.id,
                "registration_number": (
                    "AGE-MAX-"
                    f"{uuid4().hex[:8].upper()}"
                ),
            },
        )

        assert response.status_code == 400

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


def test_missing_age_reference_date_is_rejected():
    db = SessionLocal()

    user_ids = []

    competition_code = (
        "TEST-REG-NO-REF-"
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

        participant_user, _ = create_test_user(
            db,
            "user",
        )

        user_ids.extend(
            [
                admin.id,
                participant_user.id,
            ]
        )

        competition = create_test_competition(
            db,
            competition_code,
            age_reference_date=None,
        )

        group = create_test_group(
            db,
            competition.id,
            "NOREF",
            "No Reference Date",
            min_age=10,
            max_age=30,
        )

        category = create_test_category(
            db,
            competition.id,
            "NOREF",
            "No Reference Date Category",
        )

        participant = create_test_participant(
            db,
            participant_user.id,
            date(
                2005,
                1,
                1,
            ),
        )

        response = client.post(
            "/competition-registrations/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": competition.id,
                "competition_group_id": group.id,
                "competition_category_id": category.id,
                "participant_id": participant.id,
                "registration_number": (
                    "NOREF-"
                    f"{uuid4().hex[:8].upper()}"
                ),
            },
        )

        assert response.status_code == 400

    finally:
        cleanup_test_data(
            db,
            user_ids,
            competition_codes,
        )

        db.close()


# ==========================================================
# MANAGER RBAC
# ==========================================================

def test_manager_can_read_registrations():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.get(
            "/competition-registrations/",
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


def test_manager_cannot_create_registration():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.post(
            "/competition-registrations/",
            headers=authorization_header(
                token
            ),
            json={
                "competition_id": 2147483647,
                "competition_group_id": 2147483647,
                "competition_category_id": 2147483647,
                "participant_id": 2147483647,
                "registration_number": "FORBIDDEN",
            },
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_registration.create' "
                "required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_update_registration():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.put(
            (
                "/competition-registrations/"
                "2147483647"
            ),
            headers=authorization_header(
                token
            ),
            json={
                "competition_group_id": 2147483647,
                "competition_category_id": 2147483647,
                "registration_number": "FORBIDDEN",
                "status": "confirmed",
            },
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_registration.update' "
                "required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


def test_manager_cannot_delete_registration():
    db = SessionLocal()

    user_ids = []

    try:
        manager, token = create_test_user(
            db,
            "manager",
        )

        user_ids.append(manager.id)

        response = client.delete(
            (
                "/competition-registrations/"
                "2147483647"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_registration.delete' "
                "required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()


# ==========================================================
# USER RBAC
# ==========================================================

def test_user_cannot_read_registrations():
    db = SessionLocal()

    user_ids = []

    try:
        user, token = create_test_user(
            db,
            "user",
        )

        user_ids.append(user.id)

        response = client.get(
            "/competition-registrations/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 403

        assert (
            response.json()["message"]
            == (
                "Permission "
                "'competition_registration.read' "
                "required"
            )
        )

    finally:
        cleanup_test_data(
            db,
            user_ids,
            [],
        )

        db.close()