from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompetitionRoundJudgeBase(BaseModel):
    competition_round_id: int
    user_id: int
    judge_order: int | None = None
    status: str = "assigned"


class CompetitionRoundJudgeCreate(
    CompetitionRoundJudgeBase
):
    pass


class CompetitionRoundJudgeUpdate(BaseModel):
    judge_order: int | None = None
    status: str = "assigned"


class CompetitionRoundJudgeResponse(
    CompetitionRoundJudgeBase
):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )