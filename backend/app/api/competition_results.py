from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db

from app.repositories.competition_result_repository import (
    CompetitionResultRepository,
)
from app.schemas.competition_result import (
    CompetitionResultResponse,
    CompetitionRoundFinalizationResponse,
)
from app.services.competition_result_finalization_service import (
    CompetitionResultFinalizationService,
)


router = APIRouter(
    prefix="/competition-results",
    tags=["Competition Results"],
)


# ==========================================================
# ERROR MAPPING
# ==========================================================

NOT_FOUND_ERRORS = {
    "Competition round not found",
}

CONFLICT_ERRORS = {
    "Competition round results already finalized",
    "Competition round has no entries",
    "Competition round has no required judges",
    "Competition round scoring is incomplete",
}


def raise_result_error(
    exc: ValueError,
):
    detail = str(exc)

    if detail in NOT_FOUND_ERRORS:
        status_code = 404

    elif detail in CONFLICT_ERRORS:
        status_code = 409

    else:
        status_code = 400

    raise HTTPException(
        status_code=status_code,
        detail=detail,
    ) from exc


# ==========================================================
# LIST / FILTER
# ==========================================================

@router.get(
    "/",
    response_model=list[
        CompetitionResultResponse
    ],
)
def get_competition_results(
    competition_round_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_result.read"
        )
    ),
):
    repository = CompetitionResultRepository(
        db
    )

    if competition_round_id is not None:
        return repository.get_by_round(
            competition_round_id
        )

    return repository.get_all()


# ==========================================================
# DETAIL
# ==========================================================

@router.get(
    "/{result_id}",
    response_model=CompetitionResultResponse,
)
def get_competition_result(
    result_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_result.read"
        )
    ),
):
    repository = CompetitionResultRepository(
        db
    )

    result = repository.get_by_id(
        result_id
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Competition result not found",
        )

    return result


# ==========================================================
# FINALIZE ROUND
# ==========================================================

@router.post(
    "/rounds/{competition_round_id}/finalize",
    response_model=(
        CompetitionRoundFinalizationResponse
    ),
)
def finalize_competition_round(
    competition_round_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_result.finalize"
        )
    ),
):
    service = (
        CompetitionResultFinalizationService(
            db
        )
    )

    try:
        return service.finalize_round(
            competition_round_id=(
                competition_round_id
            ),
            finalized_by_user_id=(
                current_user.id
            ),
        )

    except ValueError as exc:
        raise_result_error(
            exc
        )
