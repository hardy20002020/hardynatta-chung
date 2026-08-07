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
from app.schemas.competition_result_publication import (
    CompetitionResultPublicationResponse,
)
from app.services.competition_result_finalization_service import (
    CompetitionResultFinalizationService,
)
from app.services.competition_result_publication_service import (
    CompetitionResultPublicationService,
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
    "Competition round results already approved",
    "Competition round results not finalized",
    "Competition round contains non-finalized results",
    "Competition round contains invalid finalized results",
    "Competition round results not approved",
    "Competition round results already published",
    "Competition round results are not ready for publication",
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
# PUBLICATION LIST
# ==========================================================

@router.get(
    "/publications",
    response_model=list[
        CompetitionResultPublicationResponse
    ],
)
def get_result_publications(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_result.read"
        )
    ),
):
    service = (
        CompetitionResultPublicationService(
            db
        )
    )

    return service.get_publications()


# ==========================================================
# ROUND PUBLICATION
# ==========================================================

@router.get(
    "/rounds/{competition_round_id}/publication",
    response_model=CompetitionResultPublicationResponse,
)
def get_round_result_publication(
    competition_round_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_result.read"
        )
    ),
):
    service = (
        CompetitionResultPublicationService(
            db
        )
    )

    publication = (
        service.get_publication_by_round(
            competition_round_id
        )
    )

    if publication is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition result publication "
                "not found"
            ),
        )

    return publication


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


# ==========================================================
# APPROVE ROUND RESULTS
# ==========================================================

@router.post(
    "/rounds/{competition_round_id}/approve",
    response_model=CompetitionResultPublicationResponse,
)
def approve_competition_round_results(
    competition_round_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_result.approve"
        )
    ),
):
    service = (
        CompetitionResultPublicationService(
            db
        )
    )

    try:
        return service.approve_round(
            competition_round_id=(
                competition_round_id
            ),
            approved_by_user_id=(
                current_user.id
            ),
        )

    except ValueError as exc:
        raise_result_error(
            exc
        )


# ==========================================================
# PUBLISH ROUND RESULTS
# ==========================================================

@router.post(
    "/rounds/{competition_round_id}/publish",
    response_model=CompetitionResultPublicationResponse,
)
def publish_competition_round_results(
    competition_round_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_result.publish"
        )
    ),
):
    service = (
        CompetitionResultPublicationService(
            db
        )
    )

    try:
        return service.publish_round(
            competition_round_id=(
                competition_round_id
            ),
            published_by_user_id=(
                current_user.id
            ),
        )

    except ValueError as exc:
        raise_result_error(
            exc
        )
