from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from sqlalchemy.orm import Session

from app.core.permissions import require_permission
from app.db.database import get_db
from app.schemas.competition_category import (
    CompetitionCategoryCreate,
    CompetitionCategoryResponse,
    CompetitionCategoryUpdate,
)
from app.services.competition_category_service import (
    CompetitionCategoryService,
)


router = APIRouter(
    prefix="/competition-categories",
    tags=["Competition Categories"],
)


# ==========================================================
# LIST / FILTER
# ==========================================================

@router.get(
    "/",
    response_model=list[
        CompetitionCategoryResponse
    ],
)
def get_competition_categories(
    competition_id: int | None = None,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_category.read"
        )
    ),
):
    service = CompetitionCategoryService(
        db
    )

    if competition_id is not None:
        categories = (
            service.get_categories_by_competition(
                competition_id
            )
        )

        if categories is None:
            raise HTTPException(
                status_code=404,
                detail="Competition not found",
            )

        return categories

    return service.get_categories()


# ==========================================================
# DETAIL
# ==========================================================

@router.get(
    "/{category_id}",
    response_model=CompetitionCategoryResponse,
)
def get_competition_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_category.read"
        )
    ),
):
    service = CompetitionCategoryService(
        db
    )

    category = (
        service.get_category_by_id(
            category_id
        )
    )

    if category is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition category not found"
            ),
        )

    return category


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=CompetitionCategoryResponse,
    status_code=201,
)
def create_competition_category(
    data: CompetitionCategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_category.create"
        )
    ),
):
    service = CompetitionCategoryService(
        db
    )

    try:
        return service.create_category(
            data
        )

    except ValueError as exc:
        detail = str(exc)

        if detail == "Competition not found":
            status_code = 404

        elif (
            detail
            == (
                "Competition category code "
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
    "/{category_id}",
    response_model=CompetitionCategoryResponse,
)
def update_competition_category(
    category_id: int,
    data: CompetitionCategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_category.update"
        )
    ),
):
    service = CompetitionCategoryService(
        db
    )

    try:
        category = (
            service.update_category(
                category_id,
                data,
            )
        )

    except ValueError as exc:
        detail = str(exc)

        if (
            detail
            == (
                "Competition category code "
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

    if category is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition category not found"
            ),
        )

    return category


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{category_id}",
)
def delete_competition_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission(
            "competition_category.delete"
        )
    ),
):
    service = CompetitionCategoryService(
        db
    )

    deleted = service.delete_category(
        category_id
    )

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=(
                "Competition category not found"
            ),
        )

    return {
        "success": True,
        "message": (
            "Competition category deleted "
            "successfully"
        ),
    }