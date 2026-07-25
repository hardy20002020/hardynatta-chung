from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.schemas.province import ProvinceResponse
from app.schemas.city import CityResponse


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(min_length=8)

    province_id: int | None = None
    city_id: int | None = None


class UserUpdate(BaseModel):
    name: str
    email: EmailStr

    province_id: int | None = None
    city_id: int | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    province: ProvinceResponse | None = None
    city: CityResponse | None = None

    model_config = ConfigDict(
        from_attributes=True
    )