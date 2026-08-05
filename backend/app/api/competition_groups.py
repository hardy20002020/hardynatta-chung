from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.competition_group import (
    CompetitionGroupCreate,
    CompetitionGroupResponse,
    CompetitionGroupUpdate,
)
from app.services.competition_group_service import (
    CompetitionGroupService,
)


router = APIRouter(
    prefix="/competition-groups",
    tags=["Competition Groups"],
)


@router.get(
    "/",
    response_model=list[CompetitionGroupResponse],
)
def get_competition_groups(
    competition_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_group.read"
        )
    ),
):
    service = CompetitionGroupService(db)

    if competition_id is None:
        return service.get_groups()

    groups = service.get_groups_by_competition(
        competition_id
    )

    if groups is None:
        raise HTTPException(
            status_code=404,
            detail="Competition not found",
        )

    return groups


@router.get(
    "/{group_id}",
    response_model=CompetitionGroupResponse,
)
def get_competition_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_group.read"
        )
    ),
):
    service = CompetitionGroupService(db)

    group = service.get_group_by_id(
        group_id
    )

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Competition group not found",
        )

    return group


@router.post(
    "/",
    response_model=CompetitionGroupResponse,
    status_code=201,
)
def create_competition_group(
    data: CompetitionGroupCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_group.create"
        )
    ),
):
    service = CompetitionGroupService(db)

    try:
        return service.create_group(
            data
        )

    except ValueError as exc:
        detail = str(exc)

        if detail == "Competition not found":
            status_code = 404
        else:
            status_code = 409

        raise HTTPException(
            status_code=status_code,
            detail=detail,
        ) from exc


@router.put(
    "/{group_id}",
    response_model=CompetitionGroupResponse,
)
def update_competition_group(
    group_id: int,
    data: CompetitionGroupUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_group.update"
        )
    ),
):
    service = CompetitionGroupService(db)

    try:
        group = service.update_group(
            group_id,
            data,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        ) from exc

    if group is None:
        raise HTTPException(
            status_code=404,
            detail="Competition group not found",
        )

    return group


@router.delete(
    "/{group_id}",
)
def delete_competition_group(
    group_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_group.delete"
        )
    ),
):
    service = CompetitionGroupService(db)

    deleted = service.delete_group(
        group_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Competition group not found",
        )

    return {
        "success": True,
        "message": (
            "Competition group deleted "
            "successfully"
        ),
    }