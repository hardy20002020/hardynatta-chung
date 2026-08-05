from datetime import date

from sqlalchemy.orm import Session

from app.models.chinese_surname import (
    ChineseSurname,
)
from app.models.chinese_surname_alias import (
    ChineseSurnameAlias,
)
from app.models.ethnicity import Ethnicity
from app.models.participant import Participant


class ParticipantRepository:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

    # ======================================================
    # PARTICIPANTS
    # ======================================================

    def get_all(self):
        return (
            self.db
            .query(Participant)
            .order_by(
                Participant.id
            )
            .all()
        )

    def get_by_id(
        self,
        participant_id: int,
    ):
        return (
            self.db
            .query(Participant)
            .filter(
                Participant.id
                == participant_id
            )
            .first()
        )

    def get_by_user_id(
        self,
        user_id: int,
    ):
        return (
            self.db
            .query(Participant)
            .filter(
                Participant.user_id
                == user_id
            )
            .first()
        )

    # ======================================================
    # CHINESE SURNAME MASTER DATA
    # ======================================================

    def get_chinese_surname_by_id(
        self,
        chinese_surname_id: int,
    ):
        return (
            self.db
            .query(ChineseSurname)
            .filter(
                ChineseSurname.id
                == chinese_surname_id
            )
            .first()
        )

    def get_chinese_surname_by_character(
        self,
        character: str,
    ):
        return (
            self.db
            .query(ChineseSurname)
            .filter(
                ChineseSurname.chinese_character
                == character
            )
            .first()
        )

    def get_chinese_surname_alias(
        self,
        character: str,
    ):
        return (
            self.db
            .query(ChineseSurnameAlias)
            .filter(
                ChineseSurnameAlias.character
                == character,
                ChineseSurnameAlias.is_active
                .is_(True),
            )
            .first()
        )

    def resolve_chinese_surname(
        self,
        character: str,
    ):
        """
        Resolve a Chinese surname character
        to its canonical ChineseSurname record.

        Example:

            鍾 -> surname ID 10
            锺 -> surname ID 10
            钟 -> surname ID 10
        """

        alias = self.get_chinese_surname_alias(
            character
        )

        if alias is not None:
            return (
                self.get_chinese_surname_by_id(
                    alias.chinese_surname_id
                )
            )

        return (
            self.get_chinese_surname_by_character(
                character
            )
        )

    # ======================================================
    # ETHNICITY MASTER DATA
    # ======================================================

    def get_ethnicity_by_id(
        self,
        ethnicity_id: int,
    ):
        return (
            self.db
            .query(Ethnicity)
            .filter(
                Ethnicity.id
                == ethnicity_id
            )
            .first()
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create(
        self,
        participant: Participant,
    ):
        self.db.add(participant)
        self.db.commit()
        self.db.refresh(participant)

        return participant

    # ======================================================
    # UPDATE
    # ======================================================

    def update(
        self,
        participant: Participant,
        chinese_name: str | None,
        gender: str,
        date_of_birth: date,
        chinese_surname_id: int | None,
        ethnicity_id: int | None,
        ethnicity_other: str | None,
    ):
        participant.chinese_name = chinese_name
        participant.gender = gender
        participant.date_of_birth = date_of_birth

        participant.chinese_surname_id = (
            chinese_surname_id
        )

        participant.ethnicity_id = (
            ethnicity_id
        )

        participant.ethnicity_other = (
            ethnicity_other
        )

        self.db.commit()
        self.db.refresh(participant)

        return participant

    # ======================================================
    # DELETE
    # ======================================================

    def delete(
        self,
        participant: Participant,
    ):
        self.db.delete(participant)
        self.db.commit()

        return True