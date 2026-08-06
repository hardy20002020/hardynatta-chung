from sqlalchemy.orm import Session

from app.models.competition_registration import (
    CompetitionRegistration,
)
from app.repositories.competition_category_repository import (
    CompetitionCategoryRepository,
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

        self.category_repository = (
            CompetitionCategoryRepository(db)
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
        competition_category_id: int | None = None,
    ):
        # ==================================================
        # VALIDATE COMPETITION
        # ==================================================

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

        # ==================================================
        # VALIDATE PARTICIPANT
        # ==================================================

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

        # ==================================================
        # VALIDATE CATEGORY
        # ==================================================

        if competition_category_id is not None:
            category = (
                self.category_repository
                .get_by_id(
                    competition_category_id
                )
            )

            if category is None:
                raise ValueError(
                    "Competition category not found"
                )

            if (
                competition_id is not None
                and category.competition_id
                != competition_id
            ):
                raise ValueError(
                    "Competition category does not "
                    "belong to competition"
                )

        # ==================================================
        # COMPETITION + PARTICIPANT + CATEGORY
        # ==================================================

        if (
            competition_id is not None
            and participant_id is not None
            and competition_category_id is not None
        ):
            registration = (
                self.repository
                .get_by_competition_participant_category(
                    competition_id,
                    participant_id,
                    competition_category_id,
                )
            )

            if registration is None:
                return []

            return [registration]

        # ==================================================
        # FILTER RESULT
        # ==================================================

        registrations = (
            self.repository.get_all()
        )

        if competition_id is not None:
            registrations = [
                registration
                for registration in registrations
                if (
                    registration.competition_id
                    == competition_id
                )
            ]

        if participant_id is not None:
            registrations = [
                registration
                for registration in registrations
                if (
                    registration.participant_id
                    == participant_id
                )
            ]

        if competition_category_id is not None:
            registrations = [
                registration
                for registration in registrations
                if (
                    registration.competition_category_id
                    == competition_category_id
                )
            ]

        return registrations

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
        # ==================================================
        # COMPETITION
        # ==================================================

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

        # ==================================================
        # GROUP
        # ==================================================

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

        # ==================================================
        # CATEGORY
        # ==================================================

        category = (
            self.category_repository
            .get_by_id(
                data.competition_category_id
            )
        )

        if category is None:
            raise ValueError(
                "Competition category not found"
            )

        if (
            category.competition_id
            != competition.id
        ):
            raise ValueError(
                "Competition category does not "
                "belong to competition"
            )

        # ==================================================
        # PARTICIPANT
        # ==================================================

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

        # ==================================================
        # DUPLICATE PARTICIPANT + CATEGORY
        # ==================================================

        existing_registration = (
            self.repository
            .get_by_competition_participant_category(
                competition.id,
                participant.id,
                category.id,
            )
        )

        if existing_registration is not None:
            raise ValueError(
                "Participant already registered "
                "for competition category"
            )

        # ==================================================
        # REGISTRATION NUMBER
        # ==================================================

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

        # ==================================================
        # AGE ELIGIBILITY
        # ==================================================

        CompetitionEligibilityService.validate(
            competition,
            group,
            participant,
        )

        # ==================================================
        # CREATE
        # ==================================================

        registration = CompetitionRegistration(
            competition_id=competition.id,
            competition_group_id=group.id,
            competition_category_id=category.id,
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

        # ==================================================
        # COMPETITION
        # ==================================================

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

        # ==================================================
        # GROUP
        # ==================================================

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

        # ==================================================
        # CATEGORY
        # ==================================================

        category = (
            self.category_repository
            .get_by_id(
                data.competition_category_id
            )
        )

        if category is None:
            raise ValueError(
                "Competition category not found"
            )

        if (
            category.competition_id
            != competition.id
        ):
            raise ValueError(
                "Competition category does not "
                "belong to competition"
            )

        # ==================================================
        # PARTICIPANT
        # ==================================================

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

        # ==================================================
        # DUPLICATE PARTICIPANT + CATEGORY
        # ==================================================

        existing_registration = (
            self.repository
            .get_by_competition_participant_category(
                competition.id,
                participant.id,
                category.id,
            )
        )

        if (
            existing_registration is not None
            and existing_registration.id
            != registration.id
        ):
            raise ValueError(
                "Participant already registered "
                "for competition category"
            )

        # ==================================================
        # REGISTRATION NUMBER
        # ==================================================

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

        # ==================================================
        # AGE ELIGIBILITY
        # ==================================================

        CompetitionEligibilityService.validate(
            competition,
            group,
            participant,
        )

        # ==================================================
        # UPDATE
        # ==================================================

        return self.repository.update(
            registration,
            data.competition_group_id,
            data.competition_category_id,
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