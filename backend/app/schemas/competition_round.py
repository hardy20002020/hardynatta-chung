from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ==========================================================
# COMPETITION ROUND CREATE
# ==========================================================

class CompetitionRoundCreate(BaseModel):
    competition_id: int

    code: str
    name: str
    description: str | None = None

    sort_order: int = 0
    is_active: bool = True


# ==========================================================
# COMPETITION ROUND UPDATE
# ==========================================================

class CompetitionRoundUpdate(BaseModel):
    code: str
    name: str
    description: str | None = None

    sort_order: int
    is_active: bool


# ==========================================================
# COMPETITION ROUND RESPONSE
# ==========================================================

class CompetitionRoundResponse(BaseModel):
    id: int
    competition_id: int

    code: str
    name: str
    description: str | None

    sort_order: int
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
