from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class CompetitionResultResponse(
    BaseModel
):
    id: int

    competition_round_entry_id: int

    final_score: Decimal

    rank: int

    status: str

    finalized_by_user_id: int

    finalized_at: datetime

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class CompetitionRoundFinalizationResponse(
    BaseModel
):
    competition_round_id: int

    status: str

    total_results: int

    finalized_by_user_id: int

    finalized_at: datetime

    results: list[
        CompetitionResultResponse
    ]
