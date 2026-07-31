from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.base import ApiResponse
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/",
    response_model=ApiResponse[DashboardResponse],
)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_permission("dashboard.read")),
):
    dashboard = DashboardService.get_dashboard(db)

    return ApiResponse(
        message="Dashboard loaded successfully",
        data=DashboardResponse(**dashboard),
    )