from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest
from sqlalchemy import delete

from app.core.security import hash_password
from app.db.session import SessionLocal

from app.models.audit_log import AuditLog
from app.models.competition import Competition
from app.models.competition_category import CompetitionCategory
from app.models.competition_group import CompetitionGroup
from app.models.competition_judge_score import (
    CompetitionJudgeScore,
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
from app.models.participant import Participant
from app.models.role import Role
from app.models.user import User
from app.models.user_session import UserSession

from app.services.competition_ranking_service import (
    CompetitionRankingService,
)


def create_user(
    db,
    role_name: str = "user",
):
    role = (
        db.query(Role)
        .filter(Role.name == role_name)
        .one()
    )

    user = User(
        name="Competition Ranking Test",
        email=(
            "competition-ranking-test-"
            f"{uuid4().hex}@example.com"
        ),
        password=hash_password(
            "MAJE-Ranking-2026!"
        ),
        role_id=role.id,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_ranking_context(
    db,
):
    suffix = uuid4().hex[:8]

    competition = Competition(
        name="MAJE Ranking Test",
        code=f"RK-{suffix}",
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

    group = CompetitionGroup(
        competition_id=competition.id,
        code=f"G-{suffix}",
        name="Ranking Test Group",
        min_age=0,
        max_age=100,
        sort_order=1,
        is_active=True,
    )

    category = CompetitionCategory(
        competition_id=competition.id,
        code=f"C-{suffix}",
        name="Ranking Test Category",
        sort_order=1,
        is_active=True,
    )

    competition_round = CompetitionRound(
        competition_id=competition.id,
        code=f"R-{suffix}",
        name="Ranking Test Round",
        sort_order=1,
        is_active=True,
    )

    db.add_all(
        [
            group,
            category,
            competition_round,
        ]
    )
    db.commit()

    db.refresh(group)
    db.refresh(category)
    db.refresh(competition_round)

    participant_users = []
    participants = []
    registrations = []
    entries = []

    for number in range(1, 4):
        user = create_user(db)

        participant = Participant(
            user_id=user.id,
            gender="unspecified",
            date_of_birth=date(
                2000,
                1,
                number,
            ),
        )

        db.add(participant)
        db.commit()
        db.refresh(participant)

        registration = CompetitionRegistration(
            competition_id=competition.id,
            competition_group_id=group.id,
            competition_category_id=category.id,
            participant_id=participant.id,
            registration_number=(
                f"REG-{suffix}-{number}"
            ),
            status="registered",
        )

        db.add(registration)
        db.commit()
        db.refresh(registration)

        entry = CompetitionRoundEntry(
            competition_round_id=(
                competition_round.id
            ),
            competition_registration_id=(
                registration.id
            ),
            performance_order=number,
            status="scheduled",
        )

        db.add(entry)
        db.commit()
        db.refresh(entry)

        participant_users.append(user)
        participants.append(participant)
        registrations.append(registration)
        entries.append(entry)

    judge_users = []
    judges = []

    for number in range(1, 4):
        user = create_user(db)

        judge = CompetitionRoundJudge(
            competition_round_id=(
                competition_round.id
            ),
            user_id=user.id,
            judge_order=number,
            status="assigned",
        )

        db.add(judge)
        db.commit()
        db.refresh(judge)

        judge_users.append(user)
        judges.append(judge)

    # Entry 1 average:
    # (88.6000 + 91.2000 + 89.4000) / 3
    # = 89.7333
    entry_1_scores = [
        Decimal("88.6000"),
        Decimal("91.2000"),
        Decimal("89.4000"),
    ]

    # Entry 2 average = 90.0000
    entry_2_scores = [
        Decimal("90.0000"),
        Decimal("90.0000"),
        Decimal("90.0000"),
    ]

    # Entry 3 deliberately incomplete:
    # only two of three judges submitted.
    score_matrix = [
        entry_1_scores,
        entry_2_scores,
        [
            Decimal("95.0000"),
            Decimal("95.0000"),
            None,
        ],
    ]

    scores = []

    for entry, score_values in zip(
        entries,
        score_matrix,
    ):
        for judge, total_score in zip(
            judges,
            score_values,
        ):
            if total_score is None:
                continue

            score = CompetitionJudgeScore(
                competition_round_entry_id=(
                    entry.id
                ),
                competition_round_judge_id=(
                    judge.id
                ),
                total_score=total_score,
                status="submitted",
            )

            db.add(score)
            scores.append(score)

    db.commit()

    return {
        "competition": competition,
        "round": competition_round,
        "entries": entries,
        "participant_users": participant_users,
        "judge_users": judge_users,
        "scores": scores,
    }


def cleanup_ranking_context(
    db,
    context,
):
    db.rollback()

    round_id = context["round"].id
    competition_id = context["competition"].id

    user_ids = [
        user.id
        for user in (
            context["participant_users"]
            + context["judge_users"]
        )
    ]

    entry_ids = [
        entry.id
        for entry in context["entries"]
    ]

    db.execute(
        delete(
            CompetitionJudgeScore
        ).where(
            CompetitionJudgeScore
            .competition_round_entry_id
            .in_(entry_ids)
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


def test_round_ranking_complete_and_incomplete():
    db = SessionLocal()
    context = None

    try:
        context = create_ranking_context(
            db
        )

        service = CompetitionRankingService(
            db
        )

        ranking = service.get_round_ranking(
            context["round"].id
        )

        assert ranking[
            "required_judge_count"
        ] == 3

        assert ranking[
            "total_entries"
        ] == 3

        assert ranking[
            "complete_entries"
        ] == 2

        assert ranking[
            "incomplete_entries"
        ] == 1

        results = ranking["results"]

        assert results[0]["rank"] == 1
        assert (
            results[0][
                "competition_round_entry_id"
            ]
            == context["entries"][1].id
        )
        assert (
            results[0]["final_score"]
            == Decimal("90.0000")
        )

        assert results[1]["rank"] == 2
        assert (
            results[1][
                "competition_round_entry_id"
            ]
            == context["entries"][0].id
        )
        assert (
            results[1]["final_score"]
            == Decimal("89.7333")
        )

        assert results[2]["rank"] is None
        assert (
            results[2]["status"]
            == "incomplete"
        )
        assert (
            results[2]["final_score"]
            is None
        )
        assert (
            results[2][
                "required_judge_count"
            ]
            == 3
        )
        assert (
            results[2][
                "submitted_judge_count"
            ]
            == 2
        )

    finally:
        if context is not None:
            cleanup_ranking_context(
                db,
                context,
            )

        db.close()


def test_round_ranking_shared_rank():
    db = SessionLocal()
    context = None

    try:
        context = create_ranking_context(
            db
        )

        third_entry = context["entries"][2]

        third_judge_id = (
            db.query(
                CompetitionRoundJudge
            )
            .filter(
                CompetitionRoundJudge
                .competition_round_id
                == context["round"].id
            )
            .order_by(
                CompetitionRoundJudge
                .judge_order
            )
            .all()[2].id
        )

        db.add(
            CompetitionJudgeScore(
                competition_round_entry_id=(
                    third_entry.id
                ),
                competition_round_judge_id=(
                    third_judge_id
                ),
                total_score=Decimal(
                    "80.0000"
                ),
                status="submitted",
            )
        )

        # Make entry 3 tie exactly with entry 2:
        # 95 + 95 + 80 = 270 / 3 = 90
        db.commit()

        service = CompetitionRankingService(
            db
        )

        ranking = service.get_round_ranking(
            context["round"].id
        )

        results = ranking["results"]

        assert ranking[
            "complete_entries"
        ] == 3

        assert results[0]["rank"] == 1
        assert results[1]["rank"] == 1

        assert (
            results[0]["final_score"]
            == Decimal("90.0000")
        )
        assert (
            results[1]["final_score"]
            == Decimal("90.0000")
        )

        assert results[2]["rank"] == 3
        assert (
            results[2]["final_score"]
            == Decimal("89.7333")
        )

    finally:
        if context is not None:
            cleanup_ranking_context(
                db,
                context,
            )

        db.close()


def test_round_ranking_round_not_found():
    db = SessionLocal()

    try:
        service = CompetitionRankingService(
            db
        )

        with pytest.raises(
            ValueError,
            match="Competition round not found",
        ):
            service.get_round_ranking(
                999999999
            )

    finally:
        db.close()
