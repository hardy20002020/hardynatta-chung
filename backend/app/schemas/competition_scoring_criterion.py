from datetime import datetime
from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)


class CompetitionScoringCriterionBase(BaseModel):

    code: str = Field(
        min_length=1,
        max_length=50,
    )

    name: str = Field(
        min_length=1,
        max_length=150,
    )

    description: str | None = Field(
        default=None,
        max_length=500,
    )

    weight: Decimal = Field(
        gt=Decimal("0"),
        le=Decimal("1"),
    )

    min_score: Decimal = Field(
        default=Decimal("0"),
    )

    max_score: Decimal = Field(
        default=Decimal("100"),
    )

    sort_order: int = Field(
        default=0,
        ge=0,
    )

    is_active: bool = True


class CompetitionScoringCriterionCreate(
    CompetitionScoringCriterionBase
):

    competition_round_id: int = Field(
        gt=0,
    )


class CompetitionScoringCriterionUpdate(
    CompetitionScoringCriterionBase
):
    pass


class CompetitionScoringCriterionResponse(
    CompetitionScoringCriterionBase
):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int
    competition_round_id: int

    created_at: datetime
    updated_at: datetime