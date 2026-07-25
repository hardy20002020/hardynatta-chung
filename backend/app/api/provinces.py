from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.province import (
    ProvinceCreate,
    ProvinceUpdate,
    ProvinceResponse,
)
from app.services.province_service import ProvinceService


router = APIRouter(
    prefix="/provinces",
    tags=["Provinces"],
)


@router.get(
    "/",
    response_model=list[ProvinceResponse],
)
def get_provinces(
    db: Session = Depends(get_db),
):
    return ProvinceService.get_all(db)


@router.get(
    "/{province_id}",
    response_model=ProvinceResponse,
)
def get_province(
    province_id: int,
    db: Session = Depends(get_db),
):
    province = ProvinceService.get_by_id(
        db=db,
        province_id=province_id,
    )

    if not province:
        raise HTTPException(
            status_code=404,
            detail="Province not found",
        )

    return province


@router.post(
    "/",
    response_model=ProvinceResponse,
)
def create_province(
    data: ProvinceCreate,
    db: Session = Depends(get_db),
):
    return ProvinceService.create(
        db=db,
        name=data.name,
    )


@router.put(
    "/{province_id}",
    response_model=ProvinceResponse,
)
def update_province(
    province_id: int,
    data: ProvinceUpdate,
    db: Session = Depends(get_db),
):
    province = ProvinceService.update(
        db=db,
        province_id=province_id,
        name=data.name,
    )

    if not province:
        raise HTTPException(
            status_code=404,
            detail="Province not found",
        )

    return province


@router.delete(
    "/{province_id}",
    response_model=ProvinceResponse,
)
def delete_province(
    province_id: int,
    db: Session = Depends(get_db),
):
    province = ProvinceService.delete(
        db=db,
        province_id=province_id,
    )

    if not province:
        raise HTTPException(
            status_code=404,
            detail="Province not found",
        )

    return province