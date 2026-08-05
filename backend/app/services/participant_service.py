from sqlalchemy.orm import Session

from app.models.participant import Participant
from app.repositories.participant_repository import (
    ParticipantRepository,
)
from app.repositories.user_repository import (
    UserRepository,
)
from app.schemas.participant import (
    ParticipantCreate,
    ParticipantUpdate,
)


class ParticipantService:

    VALID_GENDERS = {
        "male",
        "female",
    }

    def __init__(
        self,
        db: Session,
    ):
        self.repository = ParticipantRepository(
            db
        )

        self.user_repository = UserRepository(
            db
        )

    # ======================================================
    # PARTICIPANT READ
    # ======================================================

    def get_participants(self):
        return self.repository.get_all()

    def get_participant_by_id(
        self,
        participant_id: int,
    ):
        return self.repository.get_by_id(
            participant_id
        )

    def get_participant_by_user_id(
        self,
        user_id: int,
    ):
        return self.repository.get_by_user_id(
            user_id
        )

    # ======================================================
    # USER VALIDATION
    # ======================================================

    def _validate_user(
        self,
        user_id: int,
    ):
        user = (
            self.user_repository
            .get_user_by_id(
                user_id
            )
        )

        if user is None:
            raise ValueError(
                "User not found"
            )

        return user

    # ======================================================
    # GENDER VALIDATION
    # ======================================================

    def _normalize_gender(
        self,
        gender: str,
    ) -> str:
        normalized = gender.strip().lower()

        if normalized not in self.VALID_GENDERS:
            raise ValueError(
                "Gender must be 'male' or 'female'"
            )

        return normalized

    # ======================================================
    # CHINESE SURNAME VALIDATION
    # ======================================================

    def _validate_chinese_surname(
        self,
        chinese_surname_id: int | None,
    ):
        if chinese_surname_id is None:
            return None

        surname = (
            self.repository
            .get_chinese_surname_by_id(
                chinese_surname_id
            )
        )

        if surname is None:
            raise ValueError(
                "Chinese surname not found"
            )

        if not surname.is_active:
            raise ValueError(
                "Chinese surname is inactive"
            )

        return surname

    # ======================================================
    # ETHNICITY VALIDATION
    # ======================================================

    def _validate_ethnicity(
        self,
        ethnicity_id: int | None,
        ethnicity_other: str | None,
    ):
        if ethnicity_id is None:
            if (
                ethnicity_other is not None
                and ethnicity_other.strip()
            ):
                raise ValueError(
                    "Ethnicity must be selected "
                    "before specifying other ethnicity"
                )

            return None, None

        ethnicity = (
            self.repository
            .get_ethnicity_by_id(
                ethnicity_id
            )
        )

        if ethnicity is None:
            raise ValueError(
                "Ethnicity not found"
            )

        if not ethnicity.is_active:
            raise ValueError(
                "Ethnicity is inactive"
            )

        if ethnicity.is_other:
            if (
                ethnicity_other is None
                or not ethnicity_other.strip()
            ):
                raise ValueError(
                    "Other ethnicity must be specified"
                )

            normalized_other = (
                ethnicity_other.strip()
            )

        else:
            normalized_other = None

        return ethnicity, normalized_other

    # ======================================================
    # SURNAME RESOLUTION
    # ======================================================

    def resolve_chinese_surname(
        self,
        character: str,
    ):
        """
        Resolve registered surname variants
        to the canonical Chinese surname.

        Example:

            鍾 -> 鍾
            锺 -> 鍾
            钟 -> 鍾
        """

        normalized = character.strip()

        if not normalized:
            raise ValueError(
                "Chinese surname character is required"
            )

        surname = (
            self.repository
            .resolve_chinese_surname(
                normalized
            )
        )

        if surname is None:
            raise ValueError(
                "Chinese surname not found"
            )

        if not surname.is_active:
            raise ValueError(
                "Chinese surname is inactive"
            )

        return surname

    # ======================================================
    # CREATE
    # ======================================================

    def create_participant(
        self,
        user_id: int,
        data: ParticipantCreate,
    ):
        # User must exist before creating
        # the participant profile.
        self._validate_user(
            user_id
        )

        # One MAJE member can have only
        # one participant profile.
        existing = (
            self.repository
            .get_by_user_id(
                user_id
            )
        )

        if existing is not None:
            raise ValueError(
                "Participant profile already exists"
            )

        gender = self._normalize_gender(
            data.gender
        )

        self._validate_chinese_surname(
            data.chinese_surname_id
        )

        (
            _,
            ethnicity_other,
        ) = self._validate_ethnicity(
            data.ethnicity_id,
            data.ethnicity_other,
        )

        chinese_name = data.chinese_name

        if chinese_name is not None:
            chinese_name = (
                chinese_name.strip()
                or None
            )

        participant = Participant(
            user_id=user_id,
            chinese_name=chinese_name,
            gender=gender,
            chinese_surname_id=(
                data.chinese_surname_id
            ),
            ethnicity_id=(
                data.ethnicity_id
            ),
            ethnicity_other=(
                ethnicity_other
            ),
        )

        return self.repository.create(
            participant
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_participant(
        self,
        participant_id: int,
        data: ParticipantUpdate,
    ):
        participant = (
            self.repository
            .get_by_id(
                participant_id
            )
        )

        if participant is None:
            return None

        gender = self._normalize_gender(
            data.gender
        )

        self._validate_chinese_surname(
            data.chinese_surname_id
        )

        (
            _,
            ethnicity_other,
        ) = self._validate_ethnicity(
            data.ethnicity_id,
            data.ethnicity_other,
        )

        chinese_name = data.chinese_name

        if chinese_name is not None:
            chinese_name = (
                chinese_name.strip()
                or None
            )

        return self.repository.update(
            participant=participant,
            chinese_name=chinese_name,
            gender=gender,
            chinese_surname_id=(
                data.chinese_surname_id
            ),
            ethnicity_id=(
                data.ethnicity_id
            ),
            ethnicity_other=(
                ethnicity_other
            ),
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_participant(
        self,
        participant_id: int,
    ):
        participant = (
            self.repository
            .get_by_id(
                participant_id
            )
        )

        if participant is None:
            return False

        return self.repository.delete(
            participant
        )