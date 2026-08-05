from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ==========================================================
# COMPETITION GROUP CREATE
# ==========================================================

class CompetitionGroupCreate(BaseModel):
    competition_id: int
    code: str
    name: str

    min_age: int | None = None
    max_age: int | None = None

    sort_order: int = 0


# ==========================================================
# COMPETITION GROUP UPDATE
# ==========================================================

class CompetitionGroupUpdate(BaseModel):
    code: str
    name: str

    min_age: int | None = None
    max_age: int | None = None

    sort_order: int
    is_active: bool


# ==========================================================
# COMPETITION GROUP RESPONSE
# ==========================================================

class CompetitionGroupResponse(BaseModel):
    id: int
    competition_id: int

    code: str
    name: str

    min_age: int | None
    max_age: int | None

    sort_order: int
    is_active: bool

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )