from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.competition_round import (
    CompetitionRoundCreate,
    CompetitionRoundResponse,
    CompetitionRoundUpdate,
)
from app.services.competition_round_service import (
    CompetitionRoundService,
)


router = APIRouter(
    prefix="/competition-rounds",
    tags=["Competition Rounds"],
)


# ==========================================================
# LIST / FILTER
# ==========================================================

@router.get(
    "/",
    response_model=list[
        CompetitionRoundResponse
    ],
)
def get_competition_rounds(
    competition_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round.read"
        )
    ),
):
    service = CompetitionRoundService(
        db
    )

    if competition_id is not None:
        rounds = (
            service.get_rounds_by_competition(
                competition_id
            )
        )

        if rounds is None:
            raise HTTPException(
                status_code=404,
                detail="Competition not found",
            )

        return rounds

    return service.get_rounds()


# ==========================================================
# DETAIL
# ==========================================================

@router.get(
    "/{round_id}",
    response_model=CompetitionRoundResponse,
)
def get_competition_round(
    round_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round.read"
        )
    ),
):
    service = CompetitionRoundService(
        db
    )

    competition_round = (
        service.get_round_by_id(
            round_id
        )
    )

    if competition_round is None:
        raise HTTPException(
            status_code=404,
            detail="Competition round not found",
        )

    return competition_round


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=CompetitionRoundResponse,
    status_code=201,
)
def create_competition_round(
    data: CompetitionRoundCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round.create"
        )
    ),
):
    service = CompetitionRoundService(
        db
    )

    try:
        return service.create_round(
            data
        )

    except ValueError as exc:
        detail = str(exc)

        if detail == "Competition not found":
            status_code = 404

        elif (
            detail
            == (
                "Competition round code "
                "already exists"
            )
        ):
            status_code = 409

        else:
            status_code = 400

        raise HTTPException(
            status_code=status_code,
            detail=detail,
        ) from exc


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{round_id}",
    response_model=CompetitionRoundResponse,
)
def update_competition_round(
    round_id: int,
    data: CompetitionRoundUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round.update"
        )
    ),
):
    service = CompetitionRoundService(
        db
    )

    try:
        competition_round = (
            service.update_round(
                round_id,
                data,
            )
        )

    except ValueError as exc:
        detail = str(exc)

        if (
            detail
            == (
                "Competition round code "
                "already exists"
            )
        ):
            status_code = 409

        else:
            status_code = 400

        raise HTTPException(
            status_code=status_code,
            detail=detail,
        ) from exc

    if competition_round is None:
        raise HTTPException(
            status_code=404,
            detail="Competition round not found",
        )

    return competition_round


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{round_id}",
)
def delete_competition_round(
    round_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round.delete"
        )
    ),
):
    service = CompetitionRoundService(
        db
    )

    deleted = service.delete_round(
        round_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Competition round not found",
        )

    return {
        "success": True,
        "message": (
            "Competition round deleted "
            "successfully"
        ),
    }
