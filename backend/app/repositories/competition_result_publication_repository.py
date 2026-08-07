from sqlalchemy.orm import Session

from app.models.competition_result_publication import (
    CompetitionResultPublication,
)


class CompetitionResultPublicationRepository:

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
            .query(CompetitionResultPublication)
            .order_by(
                CompetitionResultPublication.id
            )
            .all()
        )

    def get_by_id(
        self,
        publication_id: int,
    ):
        return (
            self.db
            .query(CompetitionResultPublication)
            .filter(
                CompetitionResultPublication.id
                == publication_id
            )
            .first()
        )

    def get_by_round(
        self,
        competition_round_id: int,
    ):
        return (
            self.db
            .query(CompetitionResultPublication)
            .filter(
                CompetitionResultPublication
                .competition_round_id
                == competition_round_id
            )
            .first()
        )

    # ======================================================
    # WRITE
    # ======================================================

    def add(
        self,
        publication: CompetitionResultPublication,
    ):
        self.db.add(publication)

        return publication

    def flush(
        self,
    ):
        self.db.flush()
