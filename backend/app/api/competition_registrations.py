from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.competition_registration import (
    CompetitionRegistrationCreate,
    CompetitionRegistrationResponse,
    CompetitionRegistrationUpdate,
)
from app.services.competition_registration_service import (
    CompetitionRegistrationService,
)


router = APIRouter(
    prefix="/competition-registrations",
    tags=["Competition Registrations"],
)


# ==========================================================
# LIST / FILTER
# ==========================================================

@router.get(
    "/",
    response_model=list[
        CompetitionRegistrationResponse
    ],
)
def get_competition_registrations(
    competition_id: int | None = None,
    participant_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_registration.read"
        )
    ),
):
    service = CompetitionRegistrationService(
        db
    )

    try:
        return service.get_registrations(
            competition_id=competition_id,
            participant_id=participant_id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc


# ==========================================================
# DETAIL
# ==========================================================

@router.get(
    "/{registration_id}",
    response_model=CompetitionRegistrationResponse,
)
def get_competition_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_registration.read"
        )
    ),
):
    service = CompetitionRegistrationService(
        db
    )

    registration = (
        service.get_registration_by_id(
            registration_id
        )
    )

    if registration is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition registration "
                "not found"
            ),
        )

    return registration


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=CompetitionRegistrationResponse,
    status_code=201,
)
def create_competition_registration(
    data: CompetitionRegistrationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_registration.create"
        )
    ),
):
    service = CompetitionRegistrationService(
        db
    )

    try:
        return service.create_registration(
            data
        )

    except ValueError as exc:
        detail = str(exc)

        not_found_errors = {
            "Competition not found",
            "Competition group not found",
            "Participant not found",
        }

        conflict_errors = {
            (
                "Participant already registered "
                "for competition"
            ),
            "Registration number already exists",
        }

        if detail in not_found_errors:
            status_code = 404

        elif detail in conflict_errors:
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
    "/{registration_id}",
    response_model=CompetitionRegistrationResponse,
)
def update_competition_registration(
    registration_id: int,
    data: CompetitionRegistrationUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_registration.update"
        )
    ),
):
    service = CompetitionRegistrationService(
        db
    )

    try:
        registration = (
            service.update_registration(
                registration_id,
                data,
            )
        )

    except ValueError as exc:
        detail = str(exc)

        not_found_errors = {
            "Competition not found",
            "Competition group not found",
            "Participant not found",
        }

        if detail in not_found_errors:
            status_code = 404

        elif (
            detail
            == "Registration number already exists"
        ):
            status_code = 409

        else:
            status_code = 400

        raise HTTPException(
            status_code=status_code,
            detail=detail,
        ) from exc

    if registration is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition registration "
                "not found"
            ),
        )

    return registration


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{registration_id}",
)
def delete_competition_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_registration.delete"
        )
    ),
):
    service = CompetitionRegistrationService(
        db
    )

    deleted = service.delete_registration(
        registration_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition registration "
                "not found"
            ),
        )

    return {
        "success": True,
        "message": (
            "Competition registration "
            "deleted successfully"
        ),
    }