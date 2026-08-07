from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CompetitionResultPublicationResponse(
    BaseModel
):
    id: int

    competition_round_id: int

    status: str

    approved_by_user_id: int

    approved_at: datetime

    published_by_user_id: int | None

    published_at: datetime | None

    created_at: datetime

    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )
