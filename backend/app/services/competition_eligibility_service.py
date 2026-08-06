from datetime import date

from app.models.competition import Competition
from app.models.competition_group import (
    CompetitionGroup,
)
from app.models.participant import Participant


class CompetitionEligibilityService:

    @staticmethod
    def calculate_age(
        date_of_birth: date,
        reference_date: date,
    ) -> int:
        age = (
            reference_date.year
            - date_of_birth.year
        )

        birthday_has_not_occurred = (
            (
                reference_date.month,
                reference_date.day,
            )
            <
            (
                date_of_birth.month,
                date_of_birth.day,
            )
        )

        if birthday_has_not_occurred:
            age -= 1

        return age


    @classmethod
    def validate(
        cls,
        competition: Competition,
        group: CompetitionGroup,
        participant: Participant,
    ) -> int:
        if (
            group.competition_id
            != competition.id
        ):
            raise ValueError(
                "Competition group does not belong "
                "to competition"
            )

        if participant.date_of_birth is None:
            raise ValueError(
                "Participant date of birth is required"
            )

        if competition.age_reference_date is None:
            raise ValueError(
                "Competition age reference date "
                "is required"
            )

        age = cls.calculate_age(
            participant.date_of_birth,
            competition.age_reference_date,
        )

        if (
            group.min_age is not None
            and age < group.min_age
        ):
            raise ValueError(
                "Participant is below minimum age"
            )

        if (
            group.max_age is not None
            and age > group.max_age
        ):
            raise ValueError(
                "Participant is above maximum age"
            )

        return age