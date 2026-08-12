from app.core.time import utcnow

from sqlalchemy.orm import Session

from app.models.competition_result_publication import (
    CompetitionResultPublication,
)
from app.repositories.competition_result_publication_repository import (
    CompetitionResultPublicationRepository,
)
from app.repositories.competition_result_repository import (
    CompetitionResultRepository,
)
from app.repositories.competition_round_repository import (
    CompetitionRoundRepository,
)


class CompetitionResultPublicationService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.publication_repository = (
            CompetitionResultPublicationRepository(db)
        )

        self.result_repository = (
            CompetitionResultRepository(db)
        )

        self.round_repository = (
            CompetitionRoundRepository(db)
        )

    # ======================================================
    # READ
    # ======================================================

    def get_publications(
        self,
    ):
        return (
            self.publication_repository
            .get_all()
        )

    def get_publication_by_id(
        self,
        publication_id: int,
    ):
        return (
            self.publication_repository
            .get_by_id(
                publication_id
            )
        )

    def get_publication_by_round(
        self,
        competition_round_id: int,
    ):
        return (
            self.publication_repository
            .get_by_round(
                competition_round_id
            )
        )

    # ======================================================
    # APPROVE
    # ======================================================

    def approve_round(
        self,
        competition_round_id: int,
        approved_by_user_id: int,
    ):
        """
        Approve finalized official results for a round.

        Approval never recalculates ranking.
        It approves the immutable result snapshot
        already stored in competition_results.
        """

        try:
            # ==================================================
            # VALIDATE ROUND
            # ==================================================

            competition_round = (
                self.round_repository.get_by_id(
                    competition_round_id
                )
            )

            if competition_round is None:
                raise ValueError(
                    "Competition round not found"
                )

            # ==================================================
            # PREVENT DUPLICATE APPROVAL
            # ==================================================

            existing = (
                self.publication_repository
                .get_by_round(
                    competition_round_id
                )
            )

            if existing is not None:
                raise ValueError(
                    "Competition round results "
                    "already approved"
                )

            # ==================================================
            # REQUIRE FINALIZED RESULTS
            # ==================================================

            results = (
                self.result_repository.get_by_round(
                    competition_round_id
                )
            )

            if not results:
                raise ValueError(
                    "Competition round results "
                    "not finalized"
                )

            # ==================================================
            # VALIDATE RESULT SNAPSHOT
            # ==================================================

            for result in results:
                if result.status != "finalized":
                    raise ValueError(
                        "Competition round contains "
                        "non-finalized results"
                    )

                if (
                    result.final_score is None
                    or result.rank is None
                ):
                    raise ValueError(
                        "Competition round contains "
                        "invalid finalized results"
                    )

            # ==================================================
            # CREATE APPROVAL
            # ==================================================

            approved_at = utcnow()

            publication = (
                CompetitionResultPublication(
                    competition_round_id=(
                        competition_round_id
                    ),
                    status="approved",
                    approved_by_user_id=(
                        approved_by_user_id
                    ),
                    approved_at=approved_at,
                )
            )

            self.publication_repository.add(
                publication
            )

            self.publication_repository.flush()

            self.db.commit()

            self.db.refresh(
                publication
            )

            return publication

        except Exception:
            self.db.rollback()
            raise

    # ======================================================
    # PUBLISH
    # ======================================================

    def publish_round(
        self,
        competition_round_id: int,
        published_by_user_id: int,
    ):
        """
        Publish previously approved competition results.

        Publication does not modify or recalculate
        the finalized competition result snapshot.
        """

        try:
            # ==================================================
            # VALIDATE ROUND
            # ==================================================

            competition_round = (
                self.round_repository.get_by_id(
                    competition_round_id
                )
            )

            if competition_round is None:
                raise ValueError(
                    "Competition round not found"
                )

            # ==================================================
            # REQUIRE APPROVAL
            # ==================================================

            publication = (
                self.publication_repository
                .get_by_round(
                    competition_round_id
                )
            )

            if publication is None:
                raise ValueError(
                    "Competition round results "
                    "not approved"
                )

            # ==================================================
            # PREVENT RE-PUBLICATION
            # ==================================================

            if publication.status == "published":
                raise ValueError(
                    "Competition round results "
                    "already published"
                )

            if publication.status != "approved":
                raise ValueError(
                    "Competition round results "
                    "are not ready for publication"
                )

            # ==================================================
            # PUBLISH
            # ==================================================

            published_at = utcnow()

            publication.status = "published"

            publication.published_by_user_id = (
                published_by_user_id
            )

            publication.published_at = (
                published_at
            )

            self.publication_repository.flush()

            self.db.commit()

            self.db.refresh(
                publication
            )

            return publication

        except Exception:
            self.db.rollback()
            raise
