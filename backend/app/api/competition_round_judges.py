from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.competition_round_judge import (
    CompetitionRoundJudgeCreate,
    CompetitionRoundJudgeResponse,
    CompetitionRoundJudgeUpdate,
)
from app.services.competition_round_judge_service import (
    CompetitionRoundJudgeService,
)


router = APIRouter(
    prefix="/competition-round-judges",
    tags=["Competition Round Judges"],
)


# ==========================================================
# ERROR MAPPING
# ==========================================================

NOT_FOUND_ERRORS = {
    "Competition round not found",
    "User not found",
}


CONFLICT_ERRORS = {
    (
        "User already assigned to "
        "competition round"
    ),
}


def raise_round_judge_error(
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
        CompetitionRoundJudgeResponse
    ],
)
def get_competition_round_judges(
    competition_round_id: int | None = None,
    user_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_judge.read"
        )
    ),
):
    service = CompetitionRoundJudgeService(
        db
    )

    try:
        return service.get_judges(
            competition_round_id=(
                competition_round_id
            ),
            user_id=user_id,
        )

    except ValueError as exc:
        raise_round_judge_error(
            exc
        )


# ==========================================================
# DETAIL
# ==========================================================

@router.get(
    "/{judge_id}",
    response_model=CompetitionRoundJudgeResponse,
)
def get_competition_round_judge(
    judge_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_judge.read"
        )
    ),
):
    service = CompetitionRoundJudgeService(
        db
    )

    judge = service.get_judge_by_id(
        judge_id
    )

    if judge is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition round judge "
                "not found"
            ),
        )

    return judge


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=CompetitionRoundJudgeResponse,
    status_code=201,
)
def create_competition_round_judge(
    data: CompetitionRoundJudgeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_judge.create"
        )
    ),
):
    service = CompetitionRoundJudgeService(
        db
    )

    try:
        return service.create_judge(
            data
        )

    except ValueError as exc:
        raise_round_judge_error(
            exc
        )


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{judge_id}",
    response_model=CompetitionRoundJudgeResponse,
)
def update_competition_round_judge(
    judge_id: int,
    data: CompetitionRoundJudgeUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_judge.update"
        )
    ),
):
    service = CompetitionRoundJudgeService(
        db
    )

    judge = service.update_judge(
        judge_id,
        data,
    )

    if judge is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition round judge "
                "not found"
            ),
        )

    return judge


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{judge_id}",
)
def delete_competition_round_judge(
    judge_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_judge.delete"
        )
    ),
):
    service = CompetitionRoundJudgeService(
        db
    )

    deleted = service.delete_judge(
        judge_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition round judge "
                "not found"
            ),
        )

    return {
        "success": True,
        "message": (
            "Competition round judge "
            "deleted successfully"
        ),
    }