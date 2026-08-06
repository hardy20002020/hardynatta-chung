from sqlalchemy.orm import Session

from app.models.competition_round_judge import (
    CompetitionRoundJudge,
)
from app.repositories.competition_round_judge_repository import (
    CompetitionRoundJudgeRepository,
)
from app.repositories.competition_round_repository import (
    CompetitionRoundRepository,
)
from app.repositories.user_repository import (
    UserRepository,
)
from app.schemas.competition_round_judge import (
    CompetitionRoundJudgeCreate,
    CompetitionRoundJudgeUpdate,
)


class CompetitionRoundJudgeService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.repository = (
            CompetitionRoundJudgeRepository(
                db
            )
        )

        self.round_repository = (
            CompetitionRoundRepository(
                db
            )
        )

        self.user_repository = (
            UserRepository(
                db
            )
        )

    # ======================================================
    # READ
    # ======================================================

    def get_judges(
        self,
        competition_round_id: int | None = None,
        user_id: int | None = None,
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

        if user_id is not None:
            user = (
                self.user_repository.get_user_by_id(
                    user_id
                )
            )

            if user is None:
                raise ValueError(
                    "User not found"
                )

        if (
            competition_round_id is not None
            and user_id is not None
        ):
            judge = (
                self.repository.get_by_round_user(
                    competition_round_id,
                    user_id,
                )
            )

            if judge is None:
                return []

            return [judge]

        if competition_round_id is not None:
            return self.repository.get_by_round(
                competition_round_id
            )

        if user_id is not None:
            return self.repository.get_by_user(
                user_id
            )

        return self.repository.get_all()

    def get_judge_by_id(
        self,
        judge_id: int,
    ):
        return self.repository.get_by_id(
            judge_id
        )

    # ======================================================
    # VALIDATION
    # ======================================================

    def _validate_round_user(
        self,
        competition_round_id: int,
        user_id: int,
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

        user = (
            self.user_repository.get_user_by_id(
                user_id
            )
        )

        if user is None:
            raise ValueError(
                "User not found"
            )

        if not user.is_active:
            raise ValueError(
                "User must be active to be assigned "
                "as competition round judge"
            )

        return (
            competition_round,
            user,
        )

    # ======================================================
    # CREATE
    # ======================================================

    def create_judge(
        self,
        data: CompetitionRoundJudgeCreate,
    ):
        self._validate_round_user(
            data.competition_round_id,
            data.user_id,
        )

        existing = (
            self.repository.get_by_round_user(
                data.competition_round_id,
                data.user_id,
            )
        )

        if existing is not None:
            raise ValueError(
                "User already assigned to "
                "competition round"
            )

        judge = CompetitionRoundJudge(
            competition_round_id=(
                data.competition_round_id
            ),
            user_id=data.user_id,
            judge_order=data.judge_order,
            status=data.status,
        )

        return self.repository.create(
            judge
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_judge(
        self,
        judge_id: int,
        data: CompetitionRoundJudgeUpdate,
    ):
        judge = self.repository.get_by_id(
            judge_id
        )

        if judge is None:
            return None

        return self.repository.update(
            judge,
            judge_order=data.judge_order,
            status=data.status,
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_judge(
        self,
        judge_id: int,
    ):
        judge = self.repository.get_by_id(
            judge_id
        )

        if judge is None:
            return False

        return self.repository.delete(
            judge
        )