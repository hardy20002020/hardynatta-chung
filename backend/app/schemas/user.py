from pydantic import BaseModel, ConfigDict, EmailStr


# ==========================================================
# BASE USER
# ==========================================================

class UserBase(BaseModel):
    name: str
    email: EmailStr

    province_id: int | None = None
    city_id: int | None = None


# ==========================================================
# CREATE USER
# ==========================================================

class UserCreate(UserBase):
    password: str


# ==========================================================
# UPDATE USER
# ==========================================================

class UserUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

    province_id: int | None = None
    city_id: int | None = None

    # RBAC
    role_id: int | None = None

    # Account status
    is_active: bool | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# RESPONSE USER
# ==========================================================

class UserResponse(UserBase):
    id: int

    role: str
    role_id: int
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )