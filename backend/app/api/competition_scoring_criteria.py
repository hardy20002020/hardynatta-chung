from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.competition_scoring_criterion import (
    CompetitionScoringCriterionCreate,
    CompetitionScoringCriterionResponse,
    CompetitionScoringCriterionUpdate,
)
from app.services.competition_scoring_criterion_service import (
    CompetitionScoringCriterionService,
)


router = APIRouter(
    prefix="/competition-scoring-criteria",
    tags=["Competition Scoring Criteria"],
)


# ==========================================================
# ERROR MAPPING
# ==========================================================

NOT_FOUND_ERRORS = {
    "Competition round not found",
}


CONFLICT_ERRORS = {
    "Scoring criterion code already exists in competition round",
}


def raise_scoring_criterion_error(
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
# LIST
# ==========================================================

@router.get(
    "/",
    response_model=list[
        CompetitionScoringCriterionResponse
    ],
)
def get_scoring_criteria(
    competition_round_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_scoring_criterion.read"
        )
    ),
):
    service = CompetitionScoringCriterionService(
        db
    )

    try:
        return service.get_criteria(
            competition_round_id=(
                competition_round_id
            )
        )

    except ValueError as exc:
        raise_scoring_criterion_error(
            exc
        )


# ==========================================================
# DETAIL
# ==========================================================

@router.get(
    "/{criterion_id}",
    response_model=CompetitionScoringCriterionResponse,
)
def get_scoring_criterion(
    criterion_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_scoring_criterion.read"
        )
    ),
):
    service = CompetitionScoringCriterionService(
        db
    )

    criterion = service.get_criterion_by_id(
        criterion_id
    )

    if criterion is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition scoring criterion "
                "not found"
            ),
        )

    return criterion


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=CompetitionScoringCriterionResponse,
    status_code=201,
)
def create_scoring_criterion(
    data: CompetitionScoringCriterionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_scoring_criterion.create"
        )
    ),
):
    service = CompetitionScoringCriterionService(
        db
    )

    try:
        return service.create_criterion(
            data
        )

    except ValueError as exc:
        raise_scoring_criterion_error(
            exc
        )


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{criterion_id}",
    response_model=CompetitionScoringCriterionResponse,
)
def update_scoring_criterion(
    criterion_id: int,
    data: CompetitionScoringCriterionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_scoring_criterion.update"
        )
    ),
):
    service = CompetitionScoringCriterionService(
        db
    )

    criterion = service.update_criterion(
        criterion_id,
        data,
    )

    if criterion is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition scoring criterion "
                "not found"
            ),
        )

    return criterion


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{criterion_id}",
)
def delete_scoring_criterion(
    criterion_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_scoring_criterion.delete"
        )
    ),
):
    service = CompetitionScoringCriterionService(
        db
    )

    deleted = service.delete_criterion(
        criterion_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition scoring criterion "
                "not found"
            ),
        )

    return {
        "success": True,
        "message": (
            "Competition scoring criterion "
            "deleted successfully"
        ),
    }