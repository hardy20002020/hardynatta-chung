from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


# ==========================================================
# COMPETITION CREATE
# ==========================================================

class CompetitionCreate(BaseModel):
    name: str
    code: str
    year: int
    age_reference_date: date | None = None


# ==========================================================
# COMPETITION UPDATE
# ==========================================================

class CompetitionUpdate(BaseModel):
    name: str
    code: str
    year: int
    age_reference_date: date | None = None
    is_active: bool


# ==========================================================
# COMPETITION RESPONSE
# ==========================================================

class CompetitionResponse(BaseModel):
    id: int
    name: str
    code: str
    year: int
    age_reference_date: date | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )