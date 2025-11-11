from typing import Any, Sequence
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session
from app.core.security import get_api_key
from app.db.session import get_db
from app.crud.activities import (
    build_activity_tree,
    list_activities,
    get_activity,
)
from app.models.activity import Activity
from app.schemas.activity import ActivityOut, ActivityTree

router = APIRouter(
    prefix="/activities", tags=["activities"], dependencies=[Depends(get_api_key)]
)


@router.get(
    "",
    response_model=list[ActivityOut],
    summary="Плоский список видов деятельности",
    description="Возвращает все виды деятельности с полями `id`, `name`, `parent_id`, `depth`.",
    responses={401: {"description": "Invalid or missing API key"}},
)
def get_activities(db: Session = Depends(get_db)) -> Sequence[Activity]:
    return list_activities(db)


@router.get(
    "/tree",
    response_model=list[ActivityTree],
    summary="Дерево видов деятельности (до 3 уровней)",
    description=(
        "Возвращает иерархию видов деятельности. Глубина ограничена тремя уровнями "
        "(валидируется на уровне БД). Можно запросить всё дерево или поддерево от узла."
    ),
    responses={401: {"description": "Invalid or missing API key"}},
)
def get_activities_tree(
    db: Session = Depends(get_db),
    root_id: int | None = Query(None, description="ID корня (необязательно)"),
) -> list[dict[Any, Any]]:
    return build_activity_tree(db, root_id=root_id)


@router.get(
    "/{activity_id}",
    response_model=ActivityOut,
    summary="Получить вид деятельности по ID",
    description="Возвращает карточку вида деятельности.",
    responses={
        401: {"description": "Invalid or missing API key"},
        404: {"description": "Не найдено"},
    },
)
def get_activity_by_id(
    activity_id: int = Path(..., description="ID вида деятельности"),
    db: Session = Depends(get_db),
) -> Activity:
    act = get_activity(db, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    return act
