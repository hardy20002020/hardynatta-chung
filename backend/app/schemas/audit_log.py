from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None = None
    action: str
    resource: str
    description: str | None = None
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )