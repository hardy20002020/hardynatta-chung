from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.competition_judge_score_repository import (
    CompetitionJudgeScoreRepository,
)
from app.repositories.competition_scoring_criterion_repository import (
    CompetitionScoringCriterionRepository,
)


class CompetitionJudgeScoreService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = CompetitionJudgeScoreRepository(
            db
        )

        self.criterion_repository = (
            CompetitionScoringCriterionRepository(
                db
            )
        )

    # ======================================================
    # READ
    # ======================================================

    def get_scores(
        self,
        competition_round_entry_id: int | None = None,
        competition_round_judge_id: int | None = None,
    ):

        if (
            competition_round_entry_id is not None
            and competition_round_judge_id is not None
        ):
            score = (
                self.repository.get_by_entry_judge(
                    competition_round_entry_id,
                    competition_round_judge_id,
                )
            )

            if score is None:
                return []

            return [score]

        if competition_round_entry_id is not None:
            return self.repository.get_by_entry(
                competition_round_entry_id
            )

        if competition_round_judge_id is not None:
            return self.repository.get_by_judge(
                competition_round_judge_id
            )

        return self.repository.get_all()

    def get_score_by_id(
        self,
        score_id: int,
    ):

        return self.repository.get_by_id(
            score_id
        )

    # ======================================================
    # VALIDATION
    # ======================================================

    def validate_score_complete(
        self,
        score_id: int,
    ):

        judge_score = self.repository.get_by_id(
            score_id
        )

        if judge_score is None:
            raise ValueError(
                "Competition judge score not found"
            )

        round_entry = (
            judge_score.competition_round_entry
        )

        if round_entry is None:
            raise ValueError(
                "Competition round entry not found"
            )

        criteria = (
            self.criterion_repository.get_by_round(
                round_entry.competition_round_id
            )
        )

        active_criteria = [
            criterion
            for criterion in criteria
            if criterion.is_active
        ]

        if not active_criteria:
            raise ValueError(
                "No active scoring criteria found"
            )

        detail_by_criterion_id = {
            detail.competition_scoring_criterion_id: detail
            for detail in judge_score.score_details
        }

        for criterion in active_criteria:

            detail = detail_by_criterion_id.get(
                criterion.id
            )

            if detail is None:
                raise ValueError(
                    f"Missing score for criterion: "
                    f"{criterion.code}"
                )

            if (
                detail.score < criterion.min_score
                or detail.score > criterion.max_score
            ):
                raise ValueError(
                    f"Score for criterion "
                    f"{criterion.code} must be between "
                    f"{criterion.min_score} and "
                    f"{criterion.max_score}"
                )

        return True

    # ======================================================
    # SUBMIT
    # ======================================================

    def submit_score(
        self,
        score_id: int,
    ):

        judge_score = self.repository.get_by_id(
            score_id
        )

        if judge_score is None:
            raise ValueError(
                "Competition judge score not found"
            )

        if judge_score.status != "draft":
            raise ValueError(
                "Only draft score can be submitted"
            )

        self.validate_score_complete(
            score_id
        )

        total_score = (
            self.repository.calculate_total_score(
                score_id
            )
        )

        return self.repository.update(
            judge_score,
            total_score=total_score,
            status="submitted",
            notes=judge_score.notes,
            submitted_at=datetime.utcnow(),
        )
