from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompetitionCreate(BaseModel):
    name: str
    code: str
    year: int


class CompetitionUpdate(BaseModel):
    name: str
    code: str
    year: int
    is_active: bool


class CompetitionResponse(BaseModel):
    id: int
    name: str
    code: str
    year: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )