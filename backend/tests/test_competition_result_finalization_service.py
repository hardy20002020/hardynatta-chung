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
from app.models.competition_result import CompetitionResult
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

from app.services.competition_result_finalization_service import (
    CompetitionResultFinalizationService,
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
        name="Competition Finalization Test",
        email=(
            "competition-finalization-test-"
            f"{uuid4().hex}@example.com"
        ),
        password=hash_password(
            "MAJE-Finalization-2026!"
        ),
        role_id=role.id,
        is_active=True,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def create_finalization_context(
    db,
    *,
    complete: bool = True,
):
    suffix = uuid4().hex[:8]

    competition = Competition(
        name="MAJE Finalization Test",
        code=f"FIN-{suffix}",
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
        name="Finalization Test Group",
        min_age=0,
        max_age=100,
        sort_order=1,
        is_active=True,
    )

    category = CompetitionCategory(
        competition_id=competition.id,
        code=f"C-{suffix}",
        name="Finalization Test Category",
        sort_order=1,
        is_active=True,
    )

    competition_round = CompetitionRound(
        competition_id=competition.id,
        code=f"R-{suffix}",
        name="Finalization Test Round",
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
                f"FIN-REG-{suffix}-{number}"
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

    finalizer = create_user(
        db,
        role_name="admin",
    )

    score_matrix = [
        [
            Decimal("88.6000"),
            Decimal("91.2000"),
            Decimal("89.4000"),
        ],
        [
            Decimal("90.0000"),
            Decimal("90.0000"),
            Decimal("90.0000"),
        ],
        [
            Decimal("95.0000"),
            Decimal("95.0000"),
            Decimal("80.0000"),
        ],
    ]

    for entry_index, (
        entry,
        score_values,
    ) in enumerate(
        zip(
            entries,
            score_matrix,
        )
    ):
        for judge_index, (
            judge,
            total_score,
        ) in enumerate(
            zip(
                judges,
                score_values,
            )
        ):
            if (
                not complete
                and entry_index == 2
                and judge_index == 2
            ):
                continue

            db.add(
                CompetitionJudgeScore(
                    competition_round_entry_id=(
                        entry.id
                    ),
                    competition_round_judge_id=(
                        judge.id
                    ),
                    total_score=total_score,
                    status="submitted",
                )
            )

    db.commit()

    return {
        "competition": competition,
        "round": competition_round,
        "entries": entries,
        "participant_users": participant_users,
        "judge_users": judge_users,
        "finalizer": finalizer,
    }


def cleanup_finalization_context(
    db,
    context,
):
    db.rollback()

    round_id = context["round"].id
    competition_id = context["competition"].id

    entry_ids = [
        entry.id
        for entry in context["entries"]
    ]

    user_ids = [
        user.id
        for user in (
            context["participant_users"]
            + context["judge_users"]
            + [context["finalizer"]]
        )
    ]

    db.execute(
        delete(
            CompetitionResult
        ).where(
            CompetitionResult
            .competition_round_entry_id
            .in_(entry_ids)
        )
    )

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


def test_finalize_round_persists_official_results():
    db = SessionLocal()
    context = None

    try:
        context = create_finalization_context(
            db,
            complete=True,
        )

        service = (
            CompetitionResultFinalizationService(
                db
            )
        )

        response = service.finalize_round(
            context["round"].id,
            context["finalizer"].id,
        )

        assert response["status"] == "finalized"
        assert response["total_results"] == 3

        persisted_results = (
            db.query(CompetitionResult)
            .join(
                CompetitionRoundEntry,
                CompetitionRoundEntry.id
                == CompetitionResult
                .competition_round_entry_id,
            )
            .filter(
                CompetitionRoundEntry
                .competition_round_id
                == context["round"].id
            )
            .order_by(
                CompetitionResult.rank,
                CompetitionResult.id,
            )
            .all()
        )

        assert len(persisted_results) == 3

        assert (
            persisted_results[0]
            .competition_round_entry_id
            == context["entries"][1].id
        )
        assert (
            persisted_results[0].final_score
            == Decimal("90.0000")
        )
        assert persisted_results[0].rank == 1

        assert (
            persisted_results[1]
            .competition_round_entry_id
            == context["entries"][2].id
        )
        assert (
            persisted_results[1].final_score
            == Decimal("90.0000")
        )
        assert persisted_results[1].rank == 1

        assert (
            persisted_results[2]
            .competition_round_entry_id
            == context["entries"][0].id
        )
        assert (
            persisted_results[2].final_score
            == Decimal("89.7333")
        )
        assert persisted_results[2].rank == 3

        for result in persisted_results:
            assert result.status == "finalized"
            assert (
                result.finalized_by_user_id
                == context["finalizer"].id
            )
            assert result.finalized_at is not None

    finally:
        if context is not None:
            cleanup_finalization_context(
                db,
                context,
            )

        db.close()


def test_finalize_round_rejects_second_finalization():
    db = SessionLocal()
    context = None

    try:
        context = create_finalization_context(
            db,
            complete=True,
        )

        service = (
            CompetitionResultFinalizationService(
                db
            )
        )

        service.finalize_round(
            context["round"].id,
            context["finalizer"].id,
        )

        with pytest.raises(
            ValueError,
            match=(
                "Competition round results "
                "already finalized"
            ),
        ):
            service.finalize_round(
                context["round"].id,
                context["finalizer"].id,
            )

        result_count = (
            db.query(CompetitionResult)
            .join(
                CompetitionRoundEntry,
                CompetitionRoundEntry.id
                == CompetitionResult
                .competition_round_entry_id,
            )
            .filter(
                CompetitionRoundEntry
                .competition_round_id
                == context["round"].id
            )
            .count()
        )

        assert result_count == 3

    finally:
        if context is not None:
            cleanup_finalization_context(
                db,
                context,
            )

        db.close()


def test_finalize_round_rejects_incomplete_scoring():
    db = SessionLocal()
    context = None

    try:
        context = create_finalization_context(
            db,
            complete=False,
        )

        service = (
            CompetitionResultFinalizationService(
                db
            )
        )

        with pytest.raises(
            ValueError,
            match=(
                "Competition round scoring "
                "is incomplete"
            ),
        ):
            service.finalize_round(
                context["round"].id,
                context["finalizer"].id,
            )

        result_count = (
            db.query(CompetitionResult)
            .join(
                CompetitionRoundEntry,
                CompetitionRoundEntry.id
                == CompetitionResult
                .competition_round_entry_id,
            )
            .filter(
                CompetitionRoundEntry
                .competition_round_id
                == context["round"].id
            )
            .count()
        )

        assert result_count == 0

    finally:
        if context is not None:
            cleanup_finalization_context(
                db,
                context,
            )

        db.close()
