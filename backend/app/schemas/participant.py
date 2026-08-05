from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ==========================================================
# PARTICIPANT CREATE
# ==========================================================

class ParticipantCreate(BaseModel):
    chinese_name: str | None = None
    gender: str
    chinese_surname_id: int | None = None
    ethnicity_id: int | None = None
    ethnicity_other: str | None = None


# ==========================================================
# PARTICIPANT UPDATE
# ==========================================================

class ParticipantUpdate(BaseModel):
    chinese_name: str | None = None
    gender: str
    chinese_surname_id: int | None = None
    ethnicity_id: int | None = None
    ethnicity_other: str | None = None


# ==========================================================
# PARTICIPANT RESPONSE
# ==========================================================

class ParticipantResponse(BaseModel):
    id: int
    user_id: int

    chinese_name: str | None
    gender: str

    chinese_surname_id: int | None
    ethnicity_id: int | None
    ethnicity_other: str | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )