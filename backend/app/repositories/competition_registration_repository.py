from sqlalchemy.orm import Session

from app.models.competition_registration import (
    CompetitionRegistration,
)


class CompetitionRegistrationRepository:

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
            .query(CompetitionRegistration)
            .order_by(
                CompetitionRegistration.id.desc()
            )
            .all()
        )

    def get_by_id(
        self,
        registration_id: int,
    ):
        return (
            self.db
            .query(CompetitionRegistration)
            .filter(
                CompetitionRegistration.id
                == registration_id
            )
            .first()
        )

    def get_by_competition(
        self,
        competition_id: int,
    ):
        return (
            self.db
            .query(CompetitionRegistration)
            .filter(
                CompetitionRegistration.competition_id
                == competition_id
            )
            .order_by(
                CompetitionRegistration.id
            )
            .all()
        )

    def get_by_participant(
        self,
        participant_id: int,
    ):
        return (
            self.db
            .query(CompetitionRegistration)
            .filter(
                CompetitionRegistration.participant_id
                == participant_id
            )
            .order_by(
                CompetitionRegistration.id
            )
            .all()
        )

    def get_by_category(
        self,
        competition_category_id: int,
    ):
        return (
            self.db
            .query(CompetitionRegistration)
            .filter(
                CompetitionRegistration.competition_category_id
                == competition_category_id
            )
            .order_by(
                CompetitionRegistration.id
            )
            .all()
        )

    def get_by_competition_participant_category(
        self,
        competition_id: int,
        participant_id: int,
        competition_category_id: int,
    ):
        return (
            self.db
            .query(CompetitionRegistration)
            .filter(
                CompetitionRegistration.competition_id
                == competition_id,
                CompetitionRegistration.participant_id
                == participant_id,
                CompetitionRegistration.competition_category_id
                == competition_category_id,
            )
            .first()
        )

    def get_by_registration_number(
        self,
        competition_id: int,
        registration_number: str,
    ):
        return (
            self.db
            .query(CompetitionRegistration)
            .filter(
                CompetitionRegistration.competition_id
                == competition_id,
                CompetitionRegistration.registration_number
                == registration_number,
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        registration: CompetitionRegistration,
    ):
        self.db.add(registration)
        self.db.commit()
        self.db.refresh(registration)

        return registration

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        registration: CompetitionRegistration,
        competition_group_id: int,
        competition_category_id: int,
        registration_number: str,
        status: str,
    ):
        registration.competition_group_id = (
            competition_group_id
        )

        registration.competition_category_id = (
            competition_category_id
        )

        registration.registration_number = (
            registration_number
        )

        registration.status = status

        self.db.commit()
        self.db.refresh(registration)

        return registration

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        registration: CompetitionRegistration,
    ):
        self.db.delete(registration)
        self.db.commit()

        return True