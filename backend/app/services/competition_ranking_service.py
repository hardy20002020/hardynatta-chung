from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy.orm import Session

from app.repositories.competition_round_entry_repository import (
    CompetitionRoundEntryRepository,
)
from app.repositories.competition_round_judge_repository import (
    CompetitionRoundJudgeRepository,
)
from app.repositories.competition_round_repository import (
    CompetitionRoundRepository,
)


class CompetitionRankingService:

    ELIGIBLE_SCORE_STATUSES = {
        "submitted",
        "locked",
    }

    ELIGIBLE_JUDGE_STATUSES = {
        "assigned",
        "active",
    }

    SCORE_QUANTIZER = Decimal("0.0001")

    def __init__(
        self,
        db: Session,
    ):
        self.round_repository = (
            CompetitionRoundRepository(db)
        )

        self.entry_repository = (
            CompetitionRoundEntryRepository(db)
        )

        self.judge_repository = (
            CompetitionRoundJudgeRepository(db)
        )

    # ======================================================
    # CALCULATION
    # ======================================================

    def calculate_entry_score(
        self,
        entry,
        required_judge_ids: set[int],
    ):

        submitted_scores = {}

        for judge_score in entry.judge_scores:

            if (
                judge_score.competition_round_judge_id
                not in required_judge_ids
            ):
                continue

            if (
                judge_score.status
                not in self.ELIGIBLE_SCORE_STATUSES
            ):
                continue

            if judge_score.total_score is None:
                continue

            submitted_scores[
                judge_score.competition_round_judge_id
            ] = Decimal(
                str(judge_score.total_score)
            )

        required_judge_count = len(
            required_judge_ids
        )

        submitted_judge_count = len(
            submitted_scores
        )

        if required_judge_count == 0:
            return {
                "final_score": None,
                "status": "incomplete",
                "required_judge_count": 0,
                "submitted_judge_count": 0,
            }

        if (
            submitted_judge_count
            != required_judge_count
        ):
            return {
                "final_score": None,
                "status": "incomplete",
                "required_judge_count": (
                    required_judge_count
                ),
                "submitted_judge_count": (
                    submitted_judge_count
                ),
            }

        total = sum(
            submitted_scores.values(),
            Decimal("0"),
        )

        final_score = (
            total
            / Decimal(required_judge_count)
        ).quantize(
            self.SCORE_QUANTIZER,
            rounding=ROUND_HALF_UP,
        )

        return {
            "final_score": final_score,
            "status": "complete",
            "required_judge_count": (
                required_judge_count
            ),
            "submitted_judge_count": (
                submitted_judge_count
            ),
        }

    # ======================================================
    # RANKING
    # ======================================================

    def get_round_ranking(
        self,
        competition_round_id: int,
    ):

        competition_round = (
            self.round_repository.get_by_id(
                competition_round_id
            )
        )

        if competition_round is None:
            raise ValueError(
                "Competition round not found"
            )

        round_judges = (
            self.judge_repository.get_by_round(
                competition_round_id
            )
        )

        required_judge_ids = {
            judge.id
            for judge in round_judges
            if (
                judge.status
                in self.ELIGIBLE_JUDGE_STATUSES
            )
        }

        entries = (
            self.entry_repository.get_by_round(
                competition_round_id
            )
        )

        results = []

        for entry in entries:

            score_result = (
                self.calculate_entry_score(
                    entry,
                    required_judge_ids,
                )
            )

            results.append(
                {
                    "competition_round_entry_id": (
                        entry.id
                    ),
                    "competition_registration_id": (
                        entry.competition_registration_id
                    ),
                    "performance_order": (
                        entry.performance_order
                    ),
                    "final_score": (
                        score_result["final_score"]
                    ),
                    "status": (
                        score_result["status"]
                    ),
                    "required_judge_count": (
                        score_result[
                            "required_judge_count"
                        ]
                    ),
                    "submitted_judge_count": (
                        score_result[
                            "submitted_judge_count"
                        ]
                    ),
                    "rank": None,
                }
            )

        complete_results = [
            result
            for result in results
            if result["status"] == "complete"
        ]

        complete_results.sort(
            key=lambda result: (
                -result["final_score"],
                result[
                    "competition_round_entry_id"
                ],
            )
        )

        previous_score = None
        previous_rank = None

        for position, result in enumerate(
            complete_results,
            start=1,
        ):

            if (
                previous_score is not None
                and result["final_score"]
                == previous_score
            ):
                result["rank"] = previous_rank

            else:
                result["rank"] = position
                previous_rank = position

            previous_score = result[
                "final_score"
            ]

        incomplete_results = [
            result
            for result in results
            if result["status"] != "complete"
        ]

        incomplete_results.sort(
            key=lambda result: (
                result["performance_order"]
                is None,
                result["performance_order"]
                if result["performance_order"]
                is not None
                else 0,
                result[
                    "competition_round_entry_id"
                ],
            )
        )

        return {
            "competition_round_id": (
                competition_round_id
            ),
            "required_judge_count": len(
                required_judge_ids
            ),
            "total_entries": len(results),
            "complete_entries": len(
                complete_results
            ),
            "incomplete_entries": len(
                incomplete_results
            ),
            "results": (
                complete_results
                + incomplete_results
            ),
        }
