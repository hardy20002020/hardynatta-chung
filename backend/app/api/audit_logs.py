from fastapi import (
    APIRouter,
    Depends,
    Query,
)

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.audit_log import (
    AuditLogPaginationResponse,
)

from app.services.audit_log_service import AuditLogService



router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)



service = AuditLogService()



@router.get(
    "/",
    response_model=AuditLogPaginationResponse,
)
def get_audit_logs(

    page: int = Query(
        default=1,
        ge=1,
    ),

    size: int = Query(
        default=10,
        ge=1,
        le=100,
    ),

    user_id: int | None = Query(
        default=None,
    ),

    action: str | None = Query(
        default=None,
    ),

    db: Session = Depends(get_db),

):

    return service.get_filtered_logs(

        db,

        page=page,

        size=size,

        user_id=user_id,

        action=action,

    )