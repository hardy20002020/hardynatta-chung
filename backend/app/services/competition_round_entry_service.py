from sqlalchemy.orm import Session

from app.models.competition_round_entry import (
    CompetitionRoundEntry,
)
from app.repositories.competition_registration_repository import (
    CompetitionRegistrationRepository,
)
from app.repositories.competition_round_entry_repository import (
    CompetitionRoundEntryRepository,
)
from app.repositories.competition_round_repository import (
    CompetitionRoundRepository,
)
from app.schemas.competition_round_entry import (
    CompetitionRoundEntryCreate,
    CompetitionRoundEntryUpdate,
)


class CompetitionRoundEntryService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.repository = (
            CompetitionRoundEntryRepository(
                db
            )
        )

        self.round_repository = (
            CompetitionRoundRepository(
                db
            )
        )

        self.registration_repository = (
            CompetitionRegistrationRepository(
                db
            )
        )

    # ======================================================
    # READ
    # ======================================================

    def get_entries(
        self,
        competition_round_id: int | None = None,
        competition_registration_id: int | None = None,
    ):
        if competition_round_id is not None:
            competition_round = (
                self.round_repository.get_by_id(
                    competition_round_id
                )
            )

            if competition_round is None:
                raise ValueError(
                    "Competition round not found"
                )

        if competition_registration_id is not None:
            registration = (
                self.registration_repository.get_by_id(
                    competition_registration_id
                )
            )

            if registration is None:
                raise ValueError(
                    "Competition registration not found"
                )

        if (
            competition_round_id is not None
            and competition_registration_id is not None
        ):
            entry = (
                self.repository.get_by_round_registration(
                    competition_round_id,
                    competition_registration_id,
                )
            )

            if entry is None:
                return []

            return [entry]

        if competition_round_id is not None:
            return self.repository.get_by_round(
                competition_round_id
            )

        if competition_registration_id is not None:
            return self.repository.get_by_registration(
                competition_registration_id
            )

        return self.repository.get_all()

    def get_entry_by_id(
        self,
        entry_id: int,
    ):
        return self.repository.get_by_id(
            entry_id
        )

    # ======================================================
    # VALIDATION
    # ======================================================

    def _validate_round_registration(
        self,
        competition_round_id: int,
        competition_registration_id: int,
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

        registration = (
            self.registration_repository.get_by_id(
                competition_registration_id
            )
        )

        if registration is None:
            raise ValueError(
                "Competition registration not found"
            )

        if (
            competition_round.competition_id
            != registration.competition_id
        ):
            raise ValueError(
                "Competition round and registration "
                "must belong to the same competition"
            )

        return (
            competition_round,
            registration,
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create_entry(
        self,
        data: CompetitionRoundEntryCreate,
    ):
        self._validate_round_registration(
            data.competition_round_id,
            data.competition_registration_id,
        )

        existing = (
            self.repository.get_by_round_registration(
                data.competition_round_id,
                data.competition_registration_id,
            )
        )

        if existing is not None:
            raise ValueError(
                "Competition registration already "
                "exists in competition round"
            )

        entry = CompetitionRoundEntry(
            competition_round_id=(
                data.competition_round_id
            ),
            competition_registration_id=(
                data.competition_registration_id
            ),
            performance_order=(
                data.performance_order
            ),
            status=data.status,
        )

        return self.repository.create(
            entry
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_entry(
        self,
        entry_id: int,
        data: CompetitionRoundEntryUpdate,
    ):
        entry = self.repository.get_by_id(
            entry_id
        )

        if entry is None:
            return None

        return self.repository.update(
            entry,
            performance_order=(
                data.performance_order
            ),
            status=data.status,
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_entry(
        self,
        entry_id: int,
    ):
        entry = self.repository.get_by_id(
            entry_id
        )

        if entry is None:
            return False

        return self.repository.delete(
            entry
        )
