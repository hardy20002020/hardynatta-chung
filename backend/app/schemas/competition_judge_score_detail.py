from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
)



# ==========================================================
# BASE
# ==========================================================

class CompetitionJudgeScoreDetailBase(
    BaseModel
):

    competition_judge_score_id: int

    competition_scoring_criterion_id: int

    score: Decimal

    source: str = "human"

    notes: str | None = None



# ==========================================================
# CREATE
# ==========================================================

class CompetitionJudgeScoreDetailCreate(
    CompetitionJudgeScoreDetailBase
):
    """
    Judge input schema.

    weighted_score is calculated
    by the server.
    """

    pass



# ==========================================================
# UPDATE
# ==========================================================

class CompetitionJudgeScoreDetailUpdate(
    BaseModel
):

    score: Decimal | None = None

    source: str | None = None

    notes: str | None = None


    model_config = ConfigDict(
        from_attributes=True
    )



# ==========================================================
# RESPONSE
# ==========================================================

class CompetitionJudgeScoreDetailResponse(
    CompetitionJudgeScoreDetailBase
):

    id: int

    weighted_score: Decimal | None = None

    created_at: object

    updated_at: object


    model_config = ConfigDict(
        from_attributes=True
    )