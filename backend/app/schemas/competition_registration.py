from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ==========================================================
# COMPETITION REGISTRATION CREATE
# ==========================================================

class CompetitionRegistrationCreate(BaseModel):
    competition_id: int
    competition_group_id: int
    participant_id: int
    registration_number: str


# ==========================================================
# COMPETITION REGISTRATION UPDATE
# ==========================================================

class CompetitionRegistrationUpdate(BaseModel):
    competition_group_id: int
    registration_number: str
    status: str


# ==========================================================
# COMPETITION REGISTRATION RESPONSE
# ==========================================================

class CompetitionRegistrationResponse(BaseModel):
    id: int

    competition_id: int
    competition_group_id: int
    participant_id: int

    registration_number: str
    status: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )