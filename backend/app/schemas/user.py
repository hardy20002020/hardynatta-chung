from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    name: str
    email: EmailStr
    province_id: int
    city_id: int


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    province_id: int | None = None
    city_id: int | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class UserResponse(UserBase):
    id: int
    role_id: int

    model_config = ConfigDict(
        from_attributes=True
    )