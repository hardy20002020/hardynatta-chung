from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.participant import (
    ParticipantCreate,
    ParticipantResponse,
    ParticipantUpdate,
)
from app.services.participant_service import (
    ParticipantService,
)


router = APIRouter(
    prefix="/participants",
    tags=["Participants"],
)


# ==========================================================
# SELF-SERVICE PARTICIPANT PORTAL
# ==========================================================

@router.get(
    "/me",
    response_model=ParticipantResponse,
)
def get_my_participant_profile(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "participant.self.read"
        )
    ),
):
    service = ParticipantService(db)

    participant = (
        service.get_participant_by_user_id(
            current_user.id
        )
    )

    if participant is None:
        raise HTTPException(
            status_code=404,
            detail="Participant profile not found",
        )

    return participant


@router.post(
    "/me",
    response_model=ParticipantResponse,
    status_code=201,
)
def create_my_participant_profile(
    data: ParticipantCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "participant.self.create"
        )
    ),
):
    service = ParticipantService(db)

    try:
        return service.create_participant(
            current_user.id,
            data,
        )

    except ValueError as exc:
        detail = str(exc)

        if (
            detail
            == "Participant profile already exists"
        ):
            status_code = 409

        else:
            status_code = 400

        raise HTTPException(
            status_code=status_code,
            detail=detail,
        ) from exc


@router.put(
    "/me",
    response_model=ParticipantResponse,
)
def update_my_participant_profile(
    data: ParticipantUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "participant.self.update"
        )
    ),
):
    service = ParticipantService(db)

    participant = (
        service.get_participant_by_user_id(
            current_user.id
        )
    )

    if participant is None:
        raise HTTPException(
            status_code=404,
            detail="Participant profile not found",
        )

    try:
        updated = service.update_participant(
            participant.id,
            data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Participant profile not found",
        )

    return updated


# ==========================================================
# ADMINISTRATION - LIST
# ==========================================================

@router.get(
    "/",
    response_model=list[ParticipantResponse],
)
def get_participants(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "participant.read"
        )
    ),
):
    service = ParticipantService(db)

    return service.get_participants()


# ==========================================================
# ADMINISTRATION - CREATE
# ==========================================================

@router.post(
    "/users/{user_id}",
    response_model=ParticipantResponse,
    status_code=201,
)
def create_participant(
    user_id: int,
    data: ParticipantCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "participant.create"
        )
    ),
):
    service = ParticipantService(db)

    try:
        return service.create_participant(
            user_id,
            data,
        )

    except ValueError as exc:
        detail = str(exc)

        if detail == "User not found":
            status_code = 404

        elif (
            detail
            == "Participant profile already exists"
        ):
            status_code = 409

        else:
            status_code = 400

        raise HTTPException(
            status_code=status_code,
            detail=detail,
        ) from exc


# ==========================================================
# ADMINISTRATION - DETAIL
# ==========================================================

@router.get(
    "/{participant_id}",
    response_model=ParticipantResponse,
)
def get_participant(
    participant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "participant.read"
        )
    ),
):
    service = ParticipantService(db)

    participant = (
        service.get_participant_by_id(
            participant_id
        )
    )

    if participant is None:
        raise HTTPException(
            status_code=404,
            detail="Participant profile not found",
        )

    return participant


# ==========================================================
# ADMINISTRATION - UPDATE
# ==========================================================

@router.put(
    "/{participant_id}",
    response_model=ParticipantResponse,
)
def update_participant(
    participant_id: int,
    data: ParticipantUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "participant.update"
        )
    ),
):
    service = ParticipantService(db)

    try:
        participant = (
            service.update_participant(
                participant_id,
                data,
            )
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    if participant is None:
        raise HTTPException(
            status_code=404,
            detail="Participant profile not found",
        )

    return participant


# ==========================================================
# ADMINISTRATION - DELETE
# ==========================================================

@router.delete(
    "/{participant_id}",
)
def delete_participant(
    participant_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "participant.delete"
        )
    ),
):
    service = ParticipantService(db)

    deleted = service.delete_participant(
        participant_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Participant profile not found",
        )

    return {
        "success": True,
        "message": (
            "Participant profile deleted "
            "successfully"
        ),
    }