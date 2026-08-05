from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompetitionGroupCreate(BaseModel):
    competition_id: int
    code: str
    name: str
    sort_order: int = 0


class CompetitionGroupUpdate(BaseModel):
    code: str
    name: str
    sort_order: int
    is_active: bool


class CompetitionGroupResponse(BaseModel):
    id: int
    competition_id: int
    code: str
    name: str
    sort_order: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )