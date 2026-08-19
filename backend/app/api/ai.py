from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.ai.service import AIService
from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.ai import (
    AIGenerateRequest,
    AIGenerateResponse,
)
from app.schemas.base import ApiResponse
from app.services.audit_log_service import AuditLogService


router = APIRouter(
    prefix="/ai",
    tags=["AI"],
)


ai_service = AIService()
audit_service = AuditLogService()


@router.post(
    "/generate",
    response_model=ApiResponse[AIGenerateResponse],
)
def generate(
    request: AIGenerateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("ai.generate")
    ),
):
    result = ai_service.generate(
        request.prompt
    )

    audit_service.create_log(
        db,
        user_id=current_user.id,
        action="AI_GENERATE",
        resource="AI",
        description="AI generation request executed",
    )

    return ApiResponse(
        success=True,
        message="AI generation completed successfully",
        data=AIGenerateResponse(
            response=result,
        ),
    )
