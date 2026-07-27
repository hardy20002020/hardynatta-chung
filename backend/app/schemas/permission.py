from pydantic import BaseModel, ConfigDict


class PermissionCreate(BaseModel):
    name: str


class PermissionUpdate(BaseModel):
    name: str


class PermissionResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )
