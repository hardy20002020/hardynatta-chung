from sqlalchemy.orm import Session

from app.models.competition import Competition
from app.repositories.competition_repository import (
    CompetitionRepository,
)
from app.schemas.competition import (
    CompetitionCreate,
    CompetitionUpdate,
)


class CompetitionService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = CompetitionRepository(
            db
        )

    # ======================================================
    # READ
    # ======================================================

    def get_competitions(self):
        return self.repository.get_all()

    def get_competition_by_id(
        self,
        competition_id: int,
    ):
        return self.repository.get_by_id(
            competition_id
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create_competition(
        self,
        data: CompetitionCreate,
    ):
        existing = self.repository.get_by_code(
            data.code
        )

        if existing:
            raise ValueError(
                "Competition code already exists"
            )

        competition = Competition(
            name=data.name,
            code=data.code,
            year=data.year,
            age_reference_date=(
                data.age_reference_date
            ),
        )

        return self.repository.create(
            competition
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_competition(
        self,
        competition_id: int,
        data: CompetitionUpdate,
    ):
        competition = (
            self.repository
            .get_by_id(
                competition_id
            )
        )

        if competition is None:
            return None

        existing = self.repository.get_by_code(
            data.code
        )

        if (
            existing
            and existing.id != competition_id
        ):
            raise ValueError(
                "Competition code already exists"
            )

        return self.repository.update(
            competition=competition,
            name=data.name,
            code=data.code,
            year=data.year,
            age_reference_date=(
                data.age_reference_date
            ),
            is_active=data.is_active,
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_competition(
        self,
        competition_id: int,
    ):
        competition = (
            self.repository
            .get_by_id(
                competition_id
            )
        )

        if competition is None:
            return False

        return self.repository.delete(
            competition
        )