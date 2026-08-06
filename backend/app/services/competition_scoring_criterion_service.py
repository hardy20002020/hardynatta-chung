from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.competition_scoring_criterion import (
    CompetitionScoringCriterion,
)
from app.repositories.competition_round_repository import (
    CompetitionRoundRepository,
)
from app.repositories.competition_scoring_criterion_repository import (
    CompetitionScoringCriterionRepository,
)
from app.schemas.competition_scoring_criterion import (
    CompetitionScoringCriterionCreate,
    CompetitionScoringCriterionUpdate,
)


class CompetitionScoringCriterionService:

    def __init__(
        self,
        db: Session,
    ):
        self.db = db

        self.repository = (
            CompetitionScoringCriterionRepository(
                db
            )
        )

        self.round_repository = (
            CompetitionRoundRepository(
                db
            )
        )

    # ======================================================
    # READ
    # ======================================================

    def get_criteria(
        self,
        competition_round_id: int | None = None,
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

            return self.repository.get_by_round(
                competition_round_id
            )

        return self.repository.get_all()

    def get_criterion_by_id(
        self,
        criterion_id: int,
    ):
        return self.repository.get_by_id(
            criterion_id
        )

    # ======================================================
    # VALIDATION
    # ======================================================

    def _validate_score_range(
        self,
        min_score: Decimal,
        max_score: Decimal,
    ):
        if min_score >= max_score:
            raise ValueError(
                "Minimum score must be less "
                "than maximum score"
            )

    def _validate_round(
        self,
        competition_round_id: int,
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

        return competition_round

    def _validate_code_unique(
        self,
        competition_round_id: int,
        code: str,
        *,
        exclude_criterion_id: int | None = None,
    ):
        existing = (
            self.repository.get_by_round_code(
                competition_round_id,
                code,
            )
        )

        if existing is None:
            return

        if (
            exclude_criterion_id is not None
            and existing.id == exclude_criterion_id
        ):
            return

        raise ValueError(
            "Scoring criterion code already exists "
            "in competition round"
        )

    def _validate_total_weight(
        self,
        competition_round_id: int,
        weight: Decimal,
        is_active: bool,
        *,
        exclude_criterion_id: int | None = None,
    ):
        if not is_active:
            return

        criteria = self.repository.get_by_round(
            competition_round_id
        )

        total_weight = Decimal("0")

        for criterion in criteria:
            if (
                exclude_criterion_id is not None
                and criterion.id
                == exclude_criterion_id
            ):
                continue

            if not criterion.is_active:
                continue

            total_weight += Decimal(
                criterion.weight
            )

        total_weight += weight

        if total_weight > Decimal("1"):
            raise ValueError(
                "Total active scoring criterion "
                "weight cannot exceed 1.0000"
            )

    # ======================================================
    # CREATE
    # ======================================================

    def create_criterion(
        self,
        data: CompetitionScoringCriterionCreate,
    ):
        self._validate_round(
            data.competition_round_id
        )

        self._validate_score_range(
            data.min_score,
            data.max_score,
        )

        self._validate_code_unique(
            data.competition_round_id,
            data.code,
        )

        self._validate_total_weight(
            data.competition_round_id,
            data.weight,
            data.is_active,
        )

        criterion = CompetitionScoringCriterion(
            competition_round_id=(
                data.competition_round_id
            ),
            code=data.code,
            name=data.name,
            description=data.description,
            weight=data.weight,
            min_score=data.min_score,
            max_score=data.max_score,
            sort_order=data.sort_order,
            is_active=data.is_active,
        )

        return self.repository.create(
            criterion
        )

    # ======================================================
    # UPDATE
    # ======================================================

    def update_criterion(
        self,
        criterion_id: int,
        data: CompetitionScoringCriterionUpdate,
    ):
        criterion = self.repository.get_by_id(
            criterion_id
        )

        if criterion is None:
            return None

        self._validate_score_range(
            data.min_score,
            data.max_score,
        )

        self._validate_code_unique(
            criterion.competition_round_id,
            data.code,
            exclude_criterion_id=criterion.id,
        )

        self._validate_total_weight(
            criterion.competition_round_id,
            data.weight,
            data.is_active,
            exclude_criterion_id=criterion.id,
        )

        return self.repository.update(
            criterion,
            code=data.code,
            name=data.name,
            description=data.description,
            weight=data.weight,
            min_score=data.min_score,
            max_score=data.max_score,
            sort_order=data.sort_order,
            is_active=data.is_active,
        )

    # ======================================================
    # DELETE
    # ======================================================

    def delete_criterion(
        self,
        criterion_id: int,
    ):
        criterion = self.repository.get_by_id(
            criterion_id
        )

        if criterion is None:
            return False

        return self.repository.delete(
            criterion
        )