from sqlalchemy.orm import Session

from app.models.competition_round import (
    CompetitionRound,
)
from app.repositories.competition_repository import (
    CompetitionRepository,
)
from app.repositories.competition_round_repository import (
    CompetitionRoundRepository,
)
from app.schemas.competition_round import (
    CompetitionRoundCreate,
    CompetitionRoundUpdate,
)


class CompetitionRoundService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = (
            CompetitionRoundRepository(db)
        )

        self.competition_repository = (
            CompetitionRepository(db)
        )

    # ======================================================
    # READ
    # ======================================================

    def get_rounds(
        self,
    ):
        return self.repository.get_all()

    def get_rounds_by_competition(
        self,
        competition_id: int,
    ):
        competition = (
            self.competition_repository
            .get_by_id(
                competition_id
            )
        )

        if competition is None:
            return None

        return (
            self.repository
            .get_by_competition(
                competition_id
            )
        )

    def get_round_by_id(
        self,
        round_id: int,
    ):
        return self.repository.get_by_id(
            round_id
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create_round(
        self,
        data: CompetitionRoundCreate,
    ):
        competition = (
            self.competition_repository
            .get_by_id(
                data.competition_id
            )
        )

        if competition is None:
            raise ValueError(
                "Competition not found"
            )

        existing = (
            self.repository
            .get_by_code(
                data.competition_id,
                data.code,
            )
        )

        if existing is not None:
            raise ValueError(
                "Competition round code "
                "already exists"
            )

        competition_round = CompetitionRound(
            competition_id=data.competition_id,
            code=data.code,
            name=data.name,
            description=data.description,
            sort_order=data.sort_order,
            is_active=data.is_active,
        )

        return self.repository.create(
            competition_round
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_round(
        self,
        round_id: int,
        data: CompetitionRoundUpdate,
    ):
        competition_round = (
            self.repository.get_by_id(
                round_id
            )
        )

        if competition_round is None:
            return None

        existing = (
            self.repository
            .get_by_code(
                competition_round.competition_id,
                data.code,
            )
        )

        if (
            existing is not None
            and existing.id
            != competition_round.id
        ):
            raise ValueError(
                "Competition round code "
                "already exists"
            )

        return self.repository.update(
            competition_round,
            data.code,
            data.name,
            data.description,
            data.sort_order,
            data.is_active,
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_round(
        self,
        round_id: int,
    ):
        competition_round = (
            self.repository.get_by_id(
                round_id
            )
        )

        if competition_round is None:
            return False

        return self.repository.delete(
            competition_round
        )
