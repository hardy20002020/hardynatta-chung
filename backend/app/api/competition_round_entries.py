from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.competition_round_entry import (
    CompetitionRoundEntryCreate,
    CompetitionRoundEntryResponse,
    CompetitionRoundEntryUpdate,
)
from app.services.competition_round_entry_service import (
    CompetitionRoundEntryService,
)


router = APIRouter(
    prefix="/competition-round-entries",
    tags=["Competition Round Entries"],
)


# ==========================================================
# ERROR MAPPING
# ==========================================================

NOT_FOUND_ERRORS = {
    "Competition round not found",
    "Competition registration not found",
}


CONFLICT_ERRORS = {
    (
        "Competition registration already "
        "exists in competition round"
    ),
}


def raise_round_entry_error(
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
        CompetitionRoundEntryResponse
    ],
)
def get_competition_round_entries(
    competition_round_id: int | None = None,
    competition_registration_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_entry.read"
        )
    ),
):
    service = CompetitionRoundEntryService(
        db
    )

    try:
        return service.get_entries(
            competition_round_id=(
                competition_round_id
            ),
            competition_registration_id=(
                competition_registration_id
            ),
        )

    except ValueError as exc:
        raise_round_entry_error(
            exc
        )


# ==========================================================
# DETAIL
# ==========================================================

@router.get(
    "/{entry_id}",
    response_model=CompetitionRoundEntryResponse,
)
def get_competition_round_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_entry.read"
        )
    ),
):
    service = CompetitionRoundEntryService(
        db
    )

    entry = service.get_entry_by_id(
        entry_id
    )

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition round entry "
                "not found"
            ),
        )

    return entry


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=CompetitionRoundEntryResponse,
    status_code=201,
)
def create_competition_round_entry(
    data: CompetitionRoundEntryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_entry.create"
        )
    ),
):
    service = CompetitionRoundEntryService(
        db
    )

    try:
        return service.create_entry(
            data
        )

    except ValueError as exc:
        raise_round_entry_error(
            exc
        )


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{entry_id}",
    response_model=CompetitionRoundEntryResponse,
)
def update_competition_round_entry(
    entry_id: int,
    data: CompetitionRoundEntryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_entry.update"
        )
    ),
):
    service = CompetitionRoundEntryService(
        db
    )

    entry = service.update_entry(
        entry_id,
        data,
    )

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition round entry "
                "not found"
            ),
        )

    return entry


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{entry_id}",
)
def delete_competition_round_entry(
    entry_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_round_entry.delete"
        )
    ),
):
    service = CompetitionRoundEntryService(
        db
    )

    deleted = service.delete_entry(
        entry_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition round entry "
                "not found"
            ),
        )

    return {
        "success": True,
        "message": (
            "Competition round entry "
            "deleted successfully"
        ),
    }
