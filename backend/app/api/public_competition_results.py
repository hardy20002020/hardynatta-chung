from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.public_competition_result import (
    PublicCompetitionRoundResultResponse,
)
from app.services.public_competition_result_service import (
    PublicCompetitionResultService,
)


router = APIRouter(
    prefix="/public/competition-results",
    tags=["Public Competition Results"],
)


# ==========================================================
# PUBLIC PUBLISHED ROUND RESULT
# ==========================================================

@router.get(
    "/rounds/{competition_round_id}",
    response_model=PublicCompetitionRoundResultResponse,
)
def get_public_competition_round_result(
    competition_round_id: int,
    db: Session = Depends(get_db),
):
    """
    Return published competition results for a round.

    Authentication is intentionally not required.

    Only results whose publication state is "published"
    are exposed by the service.
    """

    service = PublicCompetitionResultService(
        db
    )

    result = service.get_published_round_result(
        competition_round_id=competition_round_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Published competition result "
                "not found"
            ),
        )

    return result
