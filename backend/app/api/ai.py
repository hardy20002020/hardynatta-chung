from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.ai.exceptions import (
    AIGatewayError,
    AIServiceDisabledError,
)
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
    try:
        result = ai_service.generate(
            request.prompt
        )
    except AIServiceDisabledError as exc:
        raise HTTPException(
            status_code=503,
            detail="AI service is currently unavailable",
        ) from exc
    except AIGatewayError as exc:
        raise HTTPException(
            status_code=502,
            detail="AI gateway request failed",
        ) from exc


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
