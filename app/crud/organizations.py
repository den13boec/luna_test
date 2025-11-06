from typing import Any, Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from app.models.organization import Organization
from app.models.building import Building
from app.models.org_activity import org_activity
from app.utils.geo import haversine_km


def get_org(db: Session, org_id: int) -> Organization | None:
    return db.get(Organization, org_id)


def list_by_building(db: Session, building_id: int) -> Sequence[Organization]:
    stmt = (
        select(Organization)
        .where(Organization.building_id == building_id)
        .order_by(Organization.id)
    )
    return db.execute(stmt).scalars().all()


def search_by_name(db: Session, q: str) -> Sequence[Organization]:
    q_like = f"%{q}%"
    stmt = (
        select(Organization)
        .where(Organization.name.ilike(q_like))
        .order_by(Organization.id)
    )
    return db.execute(stmt).scalars().all()


def list_by_activity_ids(
    db: Session, activity_ids: list[int]
) -> list[Any] | Sequence[Organization]:
    if not activity_ids:
        return []
    stmt = (
        select(Organization)
        .join(org_activity, org_activity.c.organization_id == Organization.id)
        .where(org_activity.c.activity_id.in_(activity_ids))
        .order_by(Organization.id)
    )
    return db.execute(stmt).scalars().all()


def list_in_rectangle(
    db: Session, lat_min: float, lat_max: float, lon_min: float, lon_max: float
) -> Sequence[Organization]:
    stmt = (
        select(Organization)
        .join(Building, Organization.building_id == Building.id)
        .where(
            and_(
                Building.latitude >= lat_min,
                Building.latitude <= lat_max,
                Building.longitude >= lon_min,
                Building.longitude <= lon_max,
            )
        )
        .order_by(Organization.id)
    )
    return db.execute(stmt).scalars().all()


def list_in_radius(
    db: Session, lat: float, lon: float, radius_km: float
) -> Sequence[Organization]:
    dist_expr = haversine_km(lat, lon, Building.latitude, Building.longitude)
    stmt = (
        select(Organization)
        .join(Building, Organization.building_id == Building.id)
        .where(dist_expr <= radius_km)
        .order_by(Organization.id)
    )
    return db.execute(stmt).scalars().all()
