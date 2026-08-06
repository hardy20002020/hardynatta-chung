from sqlalchemy.orm import Session

from app.models.competition_round import (
    CompetitionRound,
)


class CompetitionRoundRepository:

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
            .query(CompetitionRound)
            .order_by(
                CompetitionRound.competition_id,
                CompetitionRound.sort_order,
                CompetitionRound.id,
            )
            .all()
        )

    def get_by_competition(
        self,
        competition_id: int,
    ):
        return (
            self.db
            .query(CompetitionRound)
            .filter(
                CompetitionRound.competition_id
                == competition_id
            )
            .order_by(
                CompetitionRound.sort_order,
                CompetitionRound.id,
            )
            .all()
        )

    def get_by_id(
        self,
        round_id: int,
    ):
        return (
            self.db
            .query(CompetitionRound)
            .filter(
                CompetitionRound.id
                == round_id
            )
            .first()
        )

    def get_by_code(
        self,
        competition_id: int,
        code: str,
    ):
        return (
            self.db
            .query(CompetitionRound)
            .filter(
                CompetitionRound.competition_id
                == competition_id,
                CompetitionRound.code
                == code,
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        competition_round: CompetitionRound,
    ):
        self.db.add(
            competition_round
        )
        self.db.commit()
        self.db.refresh(
            competition_round
        )

        return competition_round

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        competition_round: CompetitionRound,
        code: str,
        name: str,
        description: str | None,
        sort_order: int,
        is_active: bool,
    ):
        competition_round.code = code
        competition_round.name = name
        competition_round.description = (
            description
        )
        competition_round.sort_order = (
            sort_order
        )
        competition_round.is_active = (
            is_active
        )

        self.db.commit()
        self.db.refresh(
            competition_round
        )

        return competition_round

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        competition_round: CompetitionRound,
    ):
        self.db.delete(
            competition_round
        )
        self.db.commit()

        return True
