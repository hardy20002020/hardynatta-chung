from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CompetitionJudgeScoreResponse(
    BaseModel
):
    id: int

    competition_round_entry_id: int

    competition_round_judge_id: int

    total_score: Decimal | None = None

    status: str

    notes: str | None = None

    submitted_at: datetime | None = None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
