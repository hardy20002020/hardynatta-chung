from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db

from app.schemas.competition_judge_score import (
    CompetitionJudgeScoreResponse,
)

from app.services.competition_judge_score_service import (
    CompetitionJudgeScoreService,
)


router = APIRouter(
    prefix="/competition-judge-scores",
    tags=["Competition Judge Scores"],
)


# ==========================================================
# ERROR MAPPING
# ==========================================================

NOT_FOUND_ERRORS = {
    "Competition judge score not found",
    "Competition round entry not found",
}

CONFLICT_ERRORS = {
    "Only draft score can be submitted",
}


def raise_judge_score_error(
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
        CompetitionJudgeScoreResponse
    ],
)
def get_competition_judge_scores(
    competition_round_entry_id: int | None = None,
    competition_round_judge_id: int | None = None,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "competition_judge_score.read"
        )
    ),
):

    service = CompetitionJudgeScoreService(
        db
    )

    return service.get_scores(
        competition_round_entry_id=(
            competition_round_entry_id
        ),
        competition_round_judge_id=(
            competition_round_judge_id
        ),
    )


# ==========================================================
# DETAIL
# ==========================================================

@router.get(
    "/{score_id}",
    response_model=CompetitionJudgeScoreResponse,
)
def get_competition_judge_score(
    score_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "competition_judge_score.read"
        )
    ),
):

    service = CompetitionJudgeScoreService(
        db
    )

    score = service.get_score_by_id(
        score_id
    )

    if score is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition judge score not found"
            ),
        )

    return score


# ==========================================================
# SUBMIT
# ==========================================================

@router.post(
    "/{score_id}/submit",
    response_model=CompetitionJudgeScoreResponse,
)
def submit_competition_judge_score(
    score_id: int,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "competition_judge_score.submit"
        )
    ),
):

    service = CompetitionJudgeScoreService(
        db
    )

    try:
        return service.submit_score(
            score_id
        )

    except ValueError as exc:
        raise_judge_score_error(
            exc
        )
