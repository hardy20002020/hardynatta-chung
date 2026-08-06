from sqlalchemy.orm import Session

from app.models.competition_round_entry import (
    CompetitionRoundEntry,
)


class CompetitionRoundEntryRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # ======================================================
    # READ
    # ======================================================

    def get_all(self):
        return (
            self.db
            .query(CompetitionRoundEntry)
            .order_by(
                CompetitionRoundEntry.competition_round_id,
                CompetitionRoundEntry.performance_order,
                CompetitionRoundEntry.id,
            )
            .all()
        )

    def get_by_id(
        self,
        entry_id: int,
    ):
        return (
            self.db
            .query(CompetitionRoundEntry)
            .filter(
                CompetitionRoundEntry.id
                == entry_id
            )
            .first()
        )

    def get_by_round(
        self,
        competition_round_id: int,
    ):
        return (
            self.db
            .query(CompetitionRoundEntry)
            .filter(
                CompetitionRoundEntry.competition_round_id
                == competition_round_id
            )
            .order_by(
                CompetitionRoundEntry.performance_order,
                CompetitionRoundEntry.id,
            )
            .all()
        )

    def get_by_registration(
        self,
        competition_registration_id: int,
    ):
        return (
            self.db
            .query(CompetitionRoundEntry)
            .filter(
                CompetitionRoundEntry.competition_registration_id
                == competition_registration_id
            )
            .order_by(
                CompetitionRoundEntry.competition_round_id,
                CompetitionRoundEntry.id,
            )
            .all()
        )

    def get_by_round_registration(
        self,
        competition_round_id: int,
        competition_registration_id: int,
    ):
        return (
            self.db
            .query(CompetitionRoundEntry)
            .filter(
                CompetitionRoundEntry.competition_round_id
                == competition_round_id,
                CompetitionRoundEntry.competition_registration_id
                == competition_registration_id,
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        entry: CompetitionRoundEntry,
    ):
        self.db.add(entry)
        self.db.commit()
        self.db.refresh(entry)

        return entry

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        entry: CompetitionRoundEntry,
        performance_order: int | None,
        status: str,
    ):
        entry.performance_order = (
            performance_order
        )

        entry.status = status

        self.db.commit()
        self.db.refresh(entry)

        return entry

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        entry: CompetitionRoundEntry,
    ):
        self.db.delete(entry)
        self.db.commit()

        return True
