from typing import Annotated, Any, Sequence
from fastapi import APIRouter, Depends, HTTPException, Path, Query
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
from app.crud.activities import get_activity_by_name, get_descendant_ids
from app.models.organization import Organization
from app.schemas.organization import OrganizationOut

router = APIRouter(
    prefix="/organizations", tags=["organizations"], dependencies=[Depends(get_api_key)]
)


@router.get(
    "/by-id/{org_id:int}",
    response_model=OrganizationOut,
    summary="Получить организацию по ID",
    description="Возвращает карточку организации с адресом, телефонами и видами деятельности.",
    responses={
        401: {"description": "Invalid or missing API key"},
        404: {"description": "Не найдено"},
    },
)
def get_organization(
    org_id: int = Path(..., description="ID организации"), db: Session = Depends(get_db)
) -> Organization:
    org = get_org(db, org_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.get(
    "/by-building/{building_id}",
    response_model=list[OrganizationOut],
    summary="Организации в здании",
    description="Возвращает все организации, закреплённые за указанным зданием.",
    responses={401: {"description": "Invalid or missing API key"}},
)
def orgs_by_building(
    building_id: int = Path(..., description="ID здания"),
    db: Session = Depends(get_db),
) -> Sequence[Organization] | list[Any]:
    return list_by_building(db, building_id)


@router.get(
    "/search",
    response_model=list[OrganizationOut],
    summary="Поиск организаций по названию",
    description="Поиск по подстроке в названии (ILIKE `%name%`).",
    responses={401: {"description": "Invalid or missing API key"}},
)
def search_organizations(
    name: str = Query(..., min_length=1, description="Подстрока названия организации"),
    db: Session = Depends(get_db),
) -> Sequence[Organization] | list[Any]:
    return search_by_name(db, name)


@router.get(
    "/by-activity-name",
    response_model=list[OrganizationOut],
    summary="Организации по названию вида деятельности (с потомками)",
    description=(
        "Ищет по названию вида деятельности. Если `deep=true`, включает все дочерние виды. "
        "Пример: name='Еда' → вернёт организации из 'Еда', 'Мясная продукция', 'Молочная продукция' и т.д."
    ),
)
def orgs_by_activity_name(
    name: str = Query(..., description="Название вида деятельности, напр. 'Еда'"),
    deep: bool = Query(True, description="Включать дочерние виды"),
    db: Session = Depends(get_db),
) -> list[Any] | list[Any] | Sequence[Organization]:
    act = get_activity_by_name(db, name)
    if not act:
        return []
    ids = get_descendant_ids(db, act.id) if deep else [act.id]
    return list_by_activity_ids(db, ids)


@router.get(
    "/near",
    response_model=list[OrganizationOut],
    summary="Организации рядом (по радиусу)",
    description=(
        "Возвращает организации в пределах заданного радиуса (км) от точки (lat, lon). "
        "Дистанция считается по сфере (Haversine/геодистанция)."
    ),
    responses={401: {"description": "Invalid or missing API key"}},
)
def orgs_near(
    lat: Annotated[float, Query(..., ge=-90, le=90, description="Широта в градусах")],
    lon: Annotated[
        float, Query(..., ge=-180, le=180, description="Долгота в градусах")
    ],
    radius_km: Annotated[float, Query(gt=0, description="Радиус в километрах")] = 1.0,
    db: Session = Depends(get_db),
) -> Sequence[Organization]:
    return list_in_radius(db, lat, lon, radius_km)


@router.get(
    "/in-rect",
    response_model=list[OrganizationOut],
    summary="Организации в прямоугольнике (bbox)",
    description=(
        "Возвращает организации, попадающие в прямоугольник по координатам "
        "`lat_min, lat_max, lon_min, lon_max`. "
        "Поддерживается пересечение антимеридиана (±180°): если `lon_min > lon_max`, "
        "область считается «обёрнутой» и выборка выполняется по двум интервалам долгот."
    ),
    responses={401: {"description": "Invalid or missing API key"}},
)
def orgs_in_rect(
    lat_min: Annotated[
        float, Query(..., ge=-90, le=90, description="Минимальная широта")
    ],
    lat_max: Annotated[
        float, Query(..., ge=-90, le=90, description="Максимальная широта")
    ],
    lon_min: Annotated[
        float, Query(..., ge=-180, le=180, description="Минимальная долгота")
    ],
    lon_max: Annotated[
        float, Query(..., ge=-180, le=180, description="Максимальная долгота")
    ],
    db: Session = Depends(get_db),
) -> Sequence[Organization]:
    return list_in_rectangle(db, lat_min, lat_max, lon_min, lon_max)
