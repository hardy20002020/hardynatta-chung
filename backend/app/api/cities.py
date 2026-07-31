from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.city import (
    CityCreate,
    CityUpdate,
    CityResponse,
)
from app.services.city_service import CityService

from app.core.permissions import require_permission


router = APIRouter(
    prefix="/cities",
    tags=["Cities"],
)


@router.get(
    "/",
    response_model=list[CityResponse],
)
def get_cities(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("city.read")
    ),
):
    return CityService.get_all(db)


@router.get(
    "/{city_id}",
    response_model=CityResponse,
)
def get_city(
    city_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("city.read")
    ),
):
    city = CityService.get_by_id(
        db=db,
        city_id=city_id,
    )

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return city


@router.post(
    "/",
    response_model=CityResponse,
)
def create_city(
    data: CityCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("city.create")
    ),
):
    return CityService.create(
        db=db,
        name=data.name,
        province_id=data.province_id,
    )


@router.put(
    "/{city_id}",
    response_model=CityResponse,
)
def update_city(
    city_id: int,
    data: CityUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("city.update")
    ),
):
    city = CityService.update(
        db=db,
        city_id=city_id,
        name=data.name,
        province_id=data.province_id,
    )

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return city


@router.delete(
    "/{city_id}",
    response_model=CityResponse,
)
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("city.delete")
    ),
):
    city = CityService.delete(
        db=db,
        city_id=city_id,
    )

    if not city:
        raise HTTPException(
            status_code=404,
            detail="City not found",
        )

    return city