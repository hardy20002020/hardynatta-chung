from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserAuthResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    role_id: int | None = None
    province_id: int | None = None
    city_id: int | None = None
    is_active: bool

    # Baru
    permissions: list[str] = []

    model_config = ConfigDict(
        from_attributes=True
    )


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserAuthResponse | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# Response Schema untuk GET /auth/me
# ==========================================================
class CurrentUserResponse(BaseModel):
    success: bool
    message: str
    user: UserAuthResponse

    model_config = ConfigDict(
        from_attributes=True
    )


# ==========================================================
# CHANGE PASSWORD
# ==========================================================

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
