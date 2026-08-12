from app.core.time import utcnow

from sqlalchemy.orm import Session

from app.models.competition_result import (
    CompetitionResult,
)
from app.repositories.competition_result_repository import (
    CompetitionResultRepository,
)
from app.services.competition_ranking_service import (
    CompetitionRankingService,
)


class CompetitionResultFinalizationService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.result_repository = (
            CompetitionResultRepository(db)
        )

        self.ranking_service = (
            CompetitionRankingService(db)
        )

    # ======================================================
    # FINALIZATION
    # ======================================================

    def finalize_round(
        self,
        competition_round_id: int,
        finalized_by_user_id: int,
    ):
        """
        Persist the official result snapshot for a round.

        Finalization is atomic:
        either every entry is persisted successfully,
        or no result from the round is persisted.
        """

        try:
            # ==================================================
            # PREVENT RE-FINALIZATION
            # ==================================================

            if self.result_repository.exists_for_round(
                competition_round_id
            ):
                raise ValueError(
                    "Competition round results "
                    "already finalized"
                )

            # ==================================================
            # CALCULATE CURRENT RANKING
            # ==================================================

            ranking = (
                self.ranking_service.get_round_ranking(
                    competition_round_id
                )
            )

            # ==================================================
            # VALIDATE ROUND CONTENT
            # ==================================================

            if ranking["total_entries"] == 0:
                raise ValueError(
                    "Competition round has no entries"
                )

            if ranking["required_judge_count"] == 0:
                raise ValueError(
                    "Competition round has no "
                    "required judges"
                )

            if ranking["incomplete_entries"] > 0:
                raise ValueError(
                    "Competition round scoring "
                    "is incomplete"
                )

            if (
                ranking["complete_entries"]
                != ranking["total_entries"]
            ):
                raise ValueError(
                    "Competition round scoring "
                    "is incomplete"
                )

            # ==================================================
            # CREATE OFFICIAL SNAPSHOT
            # ==================================================

            finalized_at = utcnow()

            results = []

            for ranking_result in ranking["results"]:

                final_score = ranking_result[
                    "final_score"
                ]

                rank = ranking_result[
                    "rank"
                ]

                if (
                    final_score is None
                    or rank is None
                ):
                    raise ValueError(
                        "Competition round contains "
                        "invalid ranking data"
                    )

                result = CompetitionResult(
                    competition_round_entry_id=(
                        ranking_result[
                            "competition_round_entry_id"
                        ]
                    ),
                    final_score=final_score,
                    rank=rank,
                    status="finalized",
                    finalized_by_user_id=(
                        finalized_by_user_id
                    ),
                    finalized_at=finalized_at,
                )

                self.result_repository.add(
                    result
                )

                results.append(
                    result
                )

            # ==================================================
            # ATOMIC DATABASE WRITE
            # ==================================================

            self.result_repository.flush()

            self.db.commit()

            for result in results:
                self.db.refresh(
                    result
                )

            return {
                "competition_round_id": (
                    competition_round_id
                ),
                "status": "finalized",
                "total_results": len(results),
                "finalized_by_user_id": (
                    finalized_by_user_id
                ),
                "finalized_at": finalized_at,
                "results": results,
            }

        except Exception:
            self.db.rollback()
            raise
