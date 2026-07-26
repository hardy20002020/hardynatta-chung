from pydantic import BaseModel


class DashboardResponse(BaseModel):
    total_users: int
    total_provinces: int
    total_cities: int
