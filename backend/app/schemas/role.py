from pydantic import BaseModel, ConfigDict


class RoleCreate(BaseModel):
    name: str


class RoleUpdate(BaseModel):
    name: str


class RoleResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )
