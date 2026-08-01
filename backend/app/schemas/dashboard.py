from pydantic import BaseModel


class DashboardResponse(BaseModel):

    # ==================================================
    # BASIC STATISTICS
    # ==================================================

    total_users: int
    total_provinces: int
    total_cities: int


    # ==================================================
    # AUDIT STATISTICS
    # ==================================================

    total_audit_logs: int = 0

    today_login: int = 0

    today_user_changes: int = 0