from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.competition import (
    CompetitionCreate,
    CompetitionResponse,
    CompetitionUpdate,
)
from app.services.competition_service import (
    CompetitionService,
)


router = APIRouter(
    prefix="/competitions",
    tags=["Competitions"],
)


@router.get(
    "/",
    response_model=list[CompetitionResponse],
)
def get_competitions(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("competition.read")
    ),
):
    service = CompetitionService(db)

    return service.get_competitions()


@router.get(
    "/{competition_id}",
    response_model=CompetitionResponse,
)
def get_competition(
    competition_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("competition.read")
    ),
):
    service = CompetitionService(db)

    competition = service.get_competition_by_id(
        competition_id
    )

    if competition is None:
        raise HTTPException(
            status_code=404,
            detail="Competition not found",
        )

    return competition


@router.post(
    "/",
    response_model=CompetitionResponse,
    status_code=201,
)
def create_competition(
    data: CompetitionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("competition.create")
    ),
):
    service = CompetitionService(db)

    try:
        return service.create_competition(
            data
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc


@router.put(
    "/{competition_id}",
    response_model=CompetitionResponse,
)
def update_competition(
    competition_id: int,
    data: CompetitionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("competition.update")
    ),
):
    service = CompetitionService(db)

    try:
        competition = (
            service.update_competition(
                competition_id,
                data,
            )
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    if competition is None:
        raise HTTPException(
            status_code=404,
            detail="Competition not found",
        )

    return competition


@router.delete(
    "/{competition_id}",
)
def delete_competition(
    competition_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("competition.delete")
    ),
):
    service = CompetitionService(db)

    deleted = service.delete_competition(
        competition_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Competition not found",
        )

    return {
        "success": True,
        "message": "Competition deleted successfully",
    }