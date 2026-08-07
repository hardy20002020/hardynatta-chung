from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db

from app.schemas.competition_judge_score_detail import (
    CompetitionJudgeScoreDetailCreate,
    CompetitionJudgeScoreDetailResponse,
    CompetitionJudgeScoreDetailUpdate,
)

from app.services.competition_judge_score_detail_service import (
    CompetitionJudgeScoreDetailService,
)


router = APIRouter(
    prefix="/competition-judge-score-details",
    tags=["Competition Judge Score Details"],
)


# ==========================================================
# ERROR MAPPING
# ==========================================================

NOT_FOUND_ERRORS = {
    "Competition judge score not found",
    "Competition scoring criterion not found",
}


CONFLICT_ERRORS = {
    "Score detail already exists",
}


def raise_score_detail_error(
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
        CompetitionJudgeScoreDetailResponse
    ],
)
def get_competition_judge_score_details(
    competition_judge_score_id: int | None = None,
    competition_scoring_criterion_id: int | None = None,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "competition_judge_score_detail.read"
        )
    ),
):

    service = CompetitionJudgeScoreDetailService(
        db
    )

    return service.get_details(
        competition_judge_score_id=(
            competition_judge_score_id
        ),

        competition_scoring_criterion_id=(
            competition_scoring_criterion_id
        ),
    )



# ==========================================================
# DETAIL
# ==========================================================

@router.get(
    "/{detail_id}",
    response_model=CompetitionJudgeScoreDetailResponse,
)
def get_competition_judge_score_detail(
    detail_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "competition_judge_score_detail.read"
        )
    ),
):

    service = CompetitionJudgeScoreDetailService(
        db
    )

    detail = service.get_detail_by_id(
        detail_id
    )

    if detail is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition judge score detail "
                "not found"
            ),
        )

    return detail



# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=CompetitionJudgeScoreDetailResponse,
    status_code=201,
)
def create_competition_judge_score_detail(
    data: CompetitionJudgeScoreDetailCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "competition_judge_score_detail.create"
        )
    ),
):

    service = CompetitionJudgeScoreDetailService(
        db
    )

    try:
        return service.create_detail(
            data
        )

    except ValueError as exc:
        raise_score_detail_error(
            exc
        )



# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{detail_id}",
    response_model=CompetitionJudgeScoreDetailResponse,
)
def update_competition_judge_score_detail(
    detail_id: int,

    data: CompetitionJudgeScoreDetailUpdate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "competition_judge_score_detail.update"
        )
    ),
):

    service = CompetitionJudgeScoreDetailService(
        db
    )

    detail = service.update_detail(
        detail_id,
        data,
    )

    if detail is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition judge score detail "
                "not found"
            ),
        )

    return detail



# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{detail_id}",
)
def delete_competition_judge_score_detail(
    detail_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "competition_judge_score_detail.delete"
        )
    ),
):

    service = CompetitionJudgeScoreDetailService(
        db
    )

    deleted = service.delete_detail(
        detail_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition judge score detail "
                "not found"
            ),
        )


    return {
        "success": True,
        "message": (
            "Competition judge score detail "
            "deleted successfully"
        ),
    }