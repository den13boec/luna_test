from typing import Any, Sequence
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.core.security import get_api_key
from app.db.session import get_db
from app.crud.organizations import (
    get_org,
    list_by_building,
    search_by_name,
    list_in_rectangle,
    list_in_radius,
    list_by_activity_ids,
)
from app.crud.activities import get_descendant_ids
from app.models.organization import Organization
from app.schemas.organization import OrganizationOut

router = APIRouter(
    prefix="/organizations", tags=["organizations"], dependencies=[Depends(get_api_key)]
)


@router.get("/{org_id}", response_model=OrganizationOut)
def get_organization(org_id: int, db: Session = Depends(get_db)) -> Organization:
    org = get_org(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get("", response_model=list[OrganizationOut])
def list_organizations(
    building_id: int | None = None,
    name: str | None = None,
    db: Session = Depends(get_db),
) -> Sequence[Organization] | list[Any]:
    if building_id is not None:
        return list_by_building(db, building_id)
    if name:
        return search_by_name(db, name)
    return []  # чтобы случайно не отдавать весь список


@router.get("/by-activity/{activity_id}", response_model=list[OrganizationOut])
def orgs_by_activity(
    activity_id: int, deep: bool = True, db: Session = Depends(get_db)
) -> list[Any] | Sequence[Organization]:
    ids = get_descendant_ids(db, activity_id) if deep else [activity_id]
    return list_by_activity_ids(db, ids)


@router.get("/near", response_model=list[OrganizationOut])
def orgs_near(
    lat: float = Query(..., description="Широта"),
    lon: float = Query(..., description="Долгота"),
    radius_km: float = Query(1.0, ge=0.0, description="Радиус в км"),
    db: Session = Depends(get_db),
) -> Sequence[Organization]:
    return list_in_radius(db, lat, lon, radius_km)


@router.get("/in-rect", response_model=list[OrganizationOut])
def orgs_in_rect(
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float,
    db: Session = Depends(get_db),
) -> Sequence[Organization]:
    return list_in_rectangle(db, lat_min, lat_max, lon_min, lon_max)
