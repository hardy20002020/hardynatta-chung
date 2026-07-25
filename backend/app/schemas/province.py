from pydantic import BaseModel, ConfigDict


class ProvinceCreate(BaseModel):
    name: str


class ProvinceUpdate(BaseModel):
    name: str


class ProvinceResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )