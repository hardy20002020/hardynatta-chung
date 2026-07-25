from pydantic import BaseModel, ConfigDict


class CityCreate(BaseModel):
    name: str
    province_id: int


class CityUpdate(BaseModel):
    name: str
    province_id: int


class CityResponse(BaseModel):
    id: int
    name: str
    province_id: int

    model_config = ConfigDict(
        from_attributes=True
    )