from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompetitionRoundEntryBase(BaseModel):
    competition_round_id: int
    competition_registration_id: int
    performance_order: int | None = None
    status: str = "scheduled"


class CompetitionRoundEntryCreate(
    CompetitionRoundEntryBase
):
    pass


class CompetitionRoundEntryUpdate(BaseModel):
    performance_order: int | None = None
    status: str


class CompetitionRoundEntryResponse(
    CompetitionRoundEntryBase
):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
