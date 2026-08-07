from datetime import date
from decimal import Decimal
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
from app.models.competition_category import CompetitionCategory
from app.models.competition_group import CompetitionGroup
from app.models.competition_judge_score import (
    CompetitionJudgeScore,
)
from app.models.competition_judge_score_detail import (
    CompetitionJudgeScoreDetail,
)
from app.models.competition_registration import (
    CompetitionRegistration,
)
from app.models.competition_round import CompetitionRound
from app.models.competition_round_entry import (
    CompetitionRoundEntry,
)
from app.models.competition_round_judge import (
    CompetitionRoundJudge,
)
from app.models.competition_scoring_criterion import (
    CompetitionScoringCriterion,
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
# USER
# ==========================================================

def create_test_user(
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

    email = (
        "competition-judge-score-api-test-"
        f"{role_name}-"
        f"{uuid4().hex}@example.com"
    )

    user = User(
        name=(
            "Competition Judge Score API Test "
            f"{role_name.title()}"
        ),
        email=email,
        password=hash_password(
            "MAJE-Judge-Score-2026!"
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
# COMPLETE SCORING CONTEXT
# ==========================================================

def create_scoring_context(
    db,
):
    suffix = uuid4().hex[:8]

    # ------------------------------------------------------
    # ADMIN
    # ------------------------------------------------------

    admin, token = create_test_user(
        db,
        "admin",
    )

    # ------------------------------------------------------
    # PARTICIPANT USER
    # ------------------------------------------------------

    participant_user, _ = create_test_user(
        db,
        "user",
    )

    participant = Participant(
        user_id=participant_user.id,
        gender="unspecified",
        date_of_birth=date(
            2000,
            1,
            1,
        ),
    )

    db.add(participant)
    db.commit()
    db.refresh(participant)

    # ------------------------------------------------------
    # JUDGE USER
    # ------------------------------------------------------

    judge_user, _ = create_test_user(
        db,
        "user",
    )

    # ------------------------------------------------------
    # COMPETITION
    # ------------------------------------------------------

    competition = Competition(
        name="MAJE Judge Score API Test",
        code=f"JS-{suffix}",
        year=2026,
        age_reference_date=date(
            2026,
            1,
            1,
        ),
    )

    db.add(competition)
    db.commit()
    db.refresh(competition)

    # ------------------------------------------------------
    # GROUP
    # ------------------------------------------------------

    group = CompetitionGroup(
        competition_id=competition.id,
        code=f"G-{suffix}",
        name="Judge Score Test Group",
        min_age=0,
        max_age=100,
        sort_order=1,
        is_active=True,
    )

    db.add(group)
    db.commit()
    db.refresh(group)

    # ------------------------------------------------------
    # CATEGORY
    # ------------------------------------------------------

    category = CompetitionCategory(
        competition_id=competition.id,
        code=f"C-{suffix}",
        name="Judge Score Test Category",
        description="API test category",
        sort_order=1,
        is_active=True,
    )

    db.add(category)
    db.commit()
    db.refresh(category)

    # ------------------------------------------------------
    # ROUND
    # ------------------------------------------------------

    competition_round = CompetitionRound(
        competition_id=competition.id,
        code=f"R-{suffix}",
        name="Judge Score Test Round",
        description="Submit score API test",
        sort_order=1,
        is_active=True,
    )

    db.add(competition_round)
    db.commit()
    db.refresh(competition_round)

    # ------------------------------------------------------
    # REGISTRATION
    # ------------------------------------------------------

    registration = CompetitionRegistration(
        competition_id=competition.id,
        competition_group_id=group.id,
        competition_category_id=category.id,
        participant_id=participant.id,
        registration_number=f"REG-{suffix}",
        status="registered",
    )

    db.add(registration)
    db.commit()
    db.refresh(registration)

    # ------------------------------------------------------
    # ROUND ENTRY
    # ------------------------------------------------------

    round_entry = CompetitionRoundEntry(
        competition_round_id=(
            competition_round.id
        ),
        competition_registration_id=(
            registration.id
        ),
        performance_order=1,
        status="scheduled",
    )

    db.add(round_entry)
    db.commit()
    db.refresh(round_entry)

    # ------------------------------------------------------
    # ROUND JUDGE
    # ------------------------------------------------------

    round_judge = CompetitionRoundJudge(
        competition_round_id=(
            competition_round.id
        ),
        user_id=judge_user.id,
        judge_order=1,
        status="assigned",
    )

    db.add(round_judge)
    db.commit()
    db.refresh(round_judge)

    # ------------------------------------------------------
    # CRITERIA
    # ------------------------------------------------------

    criterion_1 = CompetitionScoringCriterion(
        competition_round_id=(
            competition_round.id
        ),
        code="TECH",
        name="Technique",
        weight=Decimal("0.4000"),
        min_score=Decimal("0"),
        max_score=Decimal("100"),
        sort_order=1,
        is_active=True,
    )

    criterion_2 = CompetitionScoringCriterion(
        competition_round_id=(
            competition_round.id
        ),
        code="VOICE",
        name="Voice",
        weight=Decimal("0.3000"),
        min_score=Decimal("0"),
        max_score=Decimal("100"),
        sort_order=2,
        is_active=True,
    )

    criterion_3 = CompetitionScoringCriterion(
        competition_round_id=(
            competition_round.id
        ),
        code="STYLE",
        name="Style",
        weight=Decimal("0.2000"),
        min_score=Decimal("0"),
        max_score=Decimal("100"),
        sort_order=3,
        is_active=True,
    )

    criterion_4 = CompetitionScoringCriterion(
        competition_round_id=(
            competition_round.id
        ),
        code="STAGE",
        name="Stage Performance",
        weight=Decimal("0.1000"),
        min_score=Decimal("0"),
        max_score=Decimal("100"),
        sort_order=4,
        is_active=True,
    )

    db.add_all(
        [
            criterion_1,
            criterion_2,
            criterion_3,
            criterion_4,
        ]
    )

    db.commit()

    for criterion in (
        criterion_1,
        criterion_2,
        criterion_3,
        criterion_4,
    ):
        db.refresh(criterion)

    # ------------------------------------------------------
    # JUDGE SCORE
    # ------------------------------------------------------

    judge_score = CompetitionJudgeScore(
        competition_round_entry_id=(
            round_entry.id
        ),
        competition_round_judge_id=(
            round_judge.id
        ),
        status="draft",
    )

    db.add(judge_score)
    db.commit()
    db.refresh(judge_score)

    # ------------------------------------------------------
    # SCORE DETAILS
    # ------------------------------------------------------

    score_values = [
        (
            criterion_1,
            Decimal("90.0000"),
            Decimal("36.0000"),
        ),
        (
            criterion_2,
            Decimal("85.0000"),
            Decimal("25.5000"),
        ),
        (
            criterion_3,
            Decimal("88.0000"),
            Decimal("17.6000"),
        ),
        (
            criterion_4,
            Decimal("95.0000"),
            Decimal("9.5000"),
        ),
    ]

    for (
        criterion,
        raw_score,
        weighted_score,
    ) in score_values:

        detail = CompetitionJudgeScoreDetail(
            competition_judge_score_id=(
                judge_score.id
            ),
            competition_scoring_criterion_id=(
                criterion.id
            ),
            score=raw_score,
            weighted_score=weighted_score,
            source="human",
        )

        db.add(detail)

    db.commit()

    return {
        "admin": admin,
        "token": token,
        "participant_user": participant_user,
        "judge_user": judge_user,
        "participant": participant,
        "competition": competition,
        "round": competition_round,
        "entry": round_entry,
        "round_judge": round_judge,
        "score": judge_score,
    }


# ==========================================================
# CLEANUP
# ==========================================================

def cleanup_scoring_context(
    db,
    context,
):
    db.rollback()

    score_id = context["score"].id
    round_id = context["round"].id
    competition_id = context["competition"].id

    user_ids = [
        context["admin"].id,
        context["participant_user"].id,
        context["judge_user"].id,
    ]

    db.execute(
        delete(
            CompetitionJudgeScoreDetail
        ).where(
            CompetitionJudgeScoreDetail
            .competition_judge_score_id
            == score_id
        )
    )

    db.execute(
        delete(
            CompetitionJudgeScore
        ).where(
            CompetitionJudgeScore.id
            == score_id
        )
    )

    db.execute(
        delete(
            CompetitionScoringCriterion
        ).where(
            CompetitionScoringCriterion
            .competition_round_id
            == round_id
        )
    )

    db.execute(
        delete(
            CompetitionRoundJudge
        ).where(
            CompetitionRoundJudge
            .competition_round_id
            == round_id
        )
    )

    db.execute(
        delete(
            CompetitionRoundEntry
        ).where(
            CompetitionRoundEntry
            .competition_round_id
            == round_id
        )
    )

    db.execute(
        delete(
            CompetitionRegistration
        ).where(
            CompetitionRegistration
            .competition_id
            == competition_id
        )
    )

    db.execute(
        delete(
            CompetitionRound
        ).where(
            CompetitionRound.id
            == round_id
        )
    )

    db.execute(
        delete(
            CompetitionCategory
        ).where(
            CompetitionCategory
            .competition_id
            == competition_id
        )
    )

    db.execute(
        delete(
            CompetitionGroup
        ).where(
            CompetitionGroup
            .competition_id
            == competition_id
        )
    )

    db.execute(
        delete(
            Competition
        ).where(
            Competition.id
            == competition_id
        )
    )

    db.execute(
        delete(
            Participant
        ).where(
            Participant.user_id.in_(
                user_ids
            )
        )
    )

    db.execute(
        delete(
            UserSession
        ).where(
            UserSession.user_id.in_(
                user_ids
            )
        )
    )

    db.execute(
        delete(
            AuditLog
        ).where(
            AuditLog.user_id.in_(
                user_ids
            )
        )
    )

    db.execute(
        delete(
            User
        ).where(
            User.id.in_(
                user_ids
            )
        )
    )

    db.commit()


# ==========================================================
# TEST - READ + SUBMIT WORKFLOW
# ==========================================================

def test_competition_judge_score_submit_workflow():
    db = SessionLocal()

    context = None

    try:
        context = create_scoring_context(
            db
        )

        token = context["token"]
        score = context["score"]

        # --------------------------------------------------
        # LIST
        # --------------------------------------------------

        response = client.get(
            "/competition-judge-scores/",
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        assert any(
            item["id"] == score.id
            for item in response.json()
        )

        # --------------------------------------------------
        # DETAIL
        # --------------------------------------------------

        response = client.get(
            (
                "/competition-judge-scores/"
                f"{score.id}"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == score.id
        assert data["status"] == "draft"

        # --------------------------------------------------
        # FILTER BY ENTRY
        # --------------------------------------------------

        response = client.get(
            "/competition-judge-scores/",
            headers=authorization_header(
                token
            ),
            params={
                "competition_round_entry_id": (
                    context["entry"].id
                ),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == score.id

        # --------------------------------------------------
        # FILTER BY JUDGE
        # --------------------------------------------------

        response = client.get(
            "/competition-judge-scores/",
            headers=authorization_header(
                token
            ),
            params={
                "competition_round_judge_id": (
                    context["round_judge"].id
                ),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == score.id

        # --------------------------------------------------
        # FILTER ENTRY + JUDGE
        # --------------------------------------------------

        response = client.get(
            "/competition-judge-scores/",
            headers=authorization_header(
                token
            ),
            params={
                "competition_round_entry_id": (
                    context["entry"].id
                ),
                "competition_round_judge_id": (
                    context["round_judge"].id
                ),
            },
        )

        assert response.status_code == 200

        data = response.json()

        assert len(data) == 1
        assert data[0]["id"] == score.id

        # --------------------------------------------------
        # SUBMIT
        # --------------------------------------------------

        response = client.post(
            (
                "/competition-judge-scores/"
                f"{score.id}/submit"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 200

        data = response.json()

        assert data["id"] == score.id
        assert data["status"] == "submitted"

        assert Decimal(
            str(data["total_score"])
        ) == Decimal("88.6000")

        assert data["submitted_at"] is not None

        # --------------------------------------------------
        # DATABASE STATE
        # --------------------------------------------------

        db.expire_all()

        stored_score = (
            db.query(
                CompetitionJudgeScore
            )
            .filter(
                CompetitionJudgeScore.id
                == score.id
            )
            .one()
        )

        assert stored_score.status == "submitted"

        assert (
            stored_score.total_score
            == Decimal("88.6000")
        )

        assert stored_score.submitted_at is not None

        # --------------------------------------------------
        # DOUBLE SUBMIT
        # --------------------------------------------------

        response = client.post(
            (
                "/competition-judge-scores/"
                f"{score.id}/submit"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 409

        assert response.json()["message"] == (
            "Only draft score can be submitted"
        )

        # --------------------------------------------------
        # MISSING SCORE
        # --------------------------------------------------

        response = client.get(
            (
                "/competition-judge-scores/"
                "999999999"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

        response = client.post(
            (
                "/competition-judge-scores/"
                "999999999/submit"
            ),
            headers=authorization_header(
                token
            ),
        )

        assert response.status_code == 404

    finally:
        if context is not None:
            cleanup_scoring_context(
                db,
                context,
            )

        db.close()
