from sqlalchemy.orm import Session

from app.models.competition_result import (
    CompetitionResult,
)
from app.models.competition_round_entry import (
    CompetitionRoundEntry,
)


class CompetitionResultRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # ======================================================
    # READ
    # ======================================================

    def get_all(
        self,
    ):
        return (
            self.db
            .query(CompetitionResult)
            .order_by(
                CompetitionResult.id
            )
            .all()
        )

    def get_by_id(
        self,
        result_id: int,
    ):
        return (
            self.db
            .query(CompetitionResult)
            .filter(
                CompetitionResult.id
                == result_id
            )
            .first()
        )

    def get_by_entry(
        self,
        competition_round_entry_id: int,
    ):
        return (
            self.db
            .query(CompetitionResult)
            .filter(
                CompetitionResult
                .competition_round_entry_id
                == competition_round_entry_id
            )
            .first()
        )

    def get_by_round(
        self,
        competition_round_id: int,
    ):
        return (
            self.db
            .query(CompetitionResult)
            .join(
                CompetitionRoundEntry,
                CompetitionRoundEntry.id
                == CompetitionResult
                .competition_round_entry_id,
            )
            .filter(
                CompetitionRoundEntry
                .competition_round_id
                == competition_round_id
            )
            .order_by(
                CompetitionResult.rank,
                CompetitionResult.id,
            )
            .all()
        )

    def exists_for_round(
        self,
        competition_round_id: int,
    ) -> bool:
        return (
            self.db
            .query(CompetitionResult.id)
            .join(
                CompetitionRoundEntry,
                CompetitionRoundEntry.id
                == CompetitionResult
                .competition_round_entry_id,
            )
            .filter(
                CompetitionRoundEntry
                .competition_round_id
                == competition_round_id
            )
            .first()
            is not None
        )

    # ======================================================
    # WRITE
    # ======================================================

    def add(
        self,
        result: CompetitionResult,
    ):
        """
        Add a result to the current transaction.

        Commit is deliberately NOT performed here.
        Round finalization must remain atomic.
        """

        self.db.add(result)

        return result

    def flush(
        self,
    ):
        """
        Flush pending result records without committing
        the transaction.
        """

        self.db.flush()
