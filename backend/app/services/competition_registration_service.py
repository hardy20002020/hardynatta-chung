from sqlalchemy.orm import Session

from app.models.competition_registration import (
    CompetitionRegistration,
)
from app.repositories.competition_group_repository import (
    CompetitionGroupRepository,
)
from app.repositories.competition_registration_repository import (
    CompetitionRegistrationRepository,
)
from app.repositories.competition_repository import (
    CompetitionRepository,
)
from app.repositories.participant_repository import (
    ParticipantRepository,
)
from app.schemas.competition_registration import (
    CompetitionRegistrationCreate,
    CompetitionRegistrationUpdate,
)
from app.services.competition_eligibility_service import (
    CompetitionEligibilityService,
)


class CompetitionRegistrationService:

    def __init__(
        self,
        db: Session,
    ):
        self.repository = (
            CompetitionRegistrationRepository(db)
        )

        self.competition_repository = (
            CompetitionRepository(db)
        )

        self.group_repository = (
            CompetitionGroupRepository(db)
        )

        self.participant_repository = (
            ParticipantRepository(db)
        )

    # ======================================================
    # READ
    # ======================================================

    def get_registrations(
        self,
        competition_id: int | None = None,
        participant_id: int | None = None,
    ):
        if (
            competition_id is not None
            and participant_id is not None
        ):
            registration = (
                self.repository
                .get_by_competition_and_participant(
                    competition_id,
                    participant_id,
                )
            )

            if registration is None:
                return []

            return [registration]

        if competition_id is not None:
            competition = (
                self.competition_repository
                .get_by_id(
                    competition_id
                )
            )

            if competition is None:
                raise ValueError(
                    "Competition not found"
                )

            return (
                self.repository
                .get_by_competition(
                    competition_id
                )
            )

        if participant_id is not None:
            participant = (
                self.participant_repository
                .get_by_id(
                    participant_id
                )
            )

            if participant is None:
                raise ValueError(
                    "Participant not found"
                )

            return (
                self.repository
                .get_by_participant(
                    participant_id
                )
            )

        return self.repository.get_all()

    def get_registration_by_id(
        self,
        registration_id: int,
    ):
        return self.repository.get_by_id(
            registration_id
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create_registration(
        self,
        data: CompetitionRegistrationCreate,
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

        group = (
            self.group_repository
            .get_by_id(
                data.competition_group_id
            )
        )

        if group is None:
            raise ValueError(
                "Competition group not found"
            )

        participant = (
            self.participant_repository
            .get_by_id(
                data.participant_id
            )
        )

        if participant is None:
            raise ValueError(
                "Participant not found"
            )

        if (
            group.competition_id
            != competition.id
        ):
            raise ValueError(
                "Competition group does not belong "
                "to competition"
            )

        existing_participant = (
            self.repository
            .get_by_competition_and_participant(
                competition.id,
                participant.id,
            )
        )

        if existing_participant is not None:
            raise ValueError(
                "Participant already registered "
                "for competition"
            )

        existing_number = (
            self.repository
            .get_by_registration_number(
                competition.id,
                data.registration_number,
            )
        )

        if existing_number is not None:
            raise ValueError(
                "Registration number already exists"
            )

        CompetitionEligibilityService.validate(
            competition,
            group,
            participant,
        )

        registration = CompetitionRegistration(
            competition_id=competition.id,
            competition_group_id=group.id,
            participant_id=participant.id,
            registration_number=(
                data.registration_number
            ),
            status="registered",
        )

        return self.repository.create(
            registration
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_registration(
        self,
        registration_id: int,
        data: CompetitionRegistrationUpdate,
    ):
        registration = (
            self.repository.get_by_id(
                registration_id
            )
        )

        if registration is None:
            return None

        competition = (
            self.competition_repository
            .get_by_id(
                registration.competition_id
            )
        )

        if competition is None:
            raise ValueError(
                "Competition not found"
            )

        group = (
            self.group_repository
            .get_by_id(
                data.competition_group_id
            )
        )

        if group is None:
            raise ValueError(
                "Competition group not found"
            )

        if (
            group.competition_id
            != competition.id
        ):
            raise ValueError(
                "Competition group does not belong "
                "to competition"
            )

        participant = (
            self.participant_repository
            .get_by_id(
                registration.participant_id
            )
        )

        if participant is None:
            raise ValueError(
                "Participant not found"
            )

        existing_number = (
            self.repository
            .get_by_registration_number(
                competition.id,
                data.registration_number,
            )
        )

        if (
            existing_number is not None
            and existing_number.id
            != registration.id
        ):
            raise ValueError(
                "Registration number already exists"
            )

        CompetitionEligibilityService.validate(
            competition,
            group,
            participant,
        )

        return self.repository.update(
            registration,
            data.competition_group_id,
            data.registration_number,
            data.status,
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_registration(
        self,
        registration_id: int,
    ):
        registration = (
            self.repository.get_by_id(
                registration_id
            )
        )

        if registration is None:
            return False

        return self.repository.delete(
            registration
        )