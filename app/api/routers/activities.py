from typing import Any, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_api_key
from app.db.session import get_db
from app.crud.activities import list_activities, build_tree, get_activity
from app.models.activity import Activity
from app.schemas.activity import ActivityOut

router = APIRouter(
    prefix="/activities", tags=["activities"], dependencies=[Depends(get_api_key)]
)


@router.get("", response_model=list[ActivityOut])
def get_activities(db: Session = Depends(get_db)) -> Sequence[Activity]:
    return list_activities(db)


@router.get("/tree")
def get_activities_tree(db: Session = Depends(get_db)) -> list[dict[Any, Any]]:
    items = list_activities(db)
    return build_tree(items)


@router.get("/{activity_id}", response_model=ActivityOut)
def get_activity_by_id(activity_id: int, db: Session = Depends(get_db)) -> Activity:
    act = get_activity(db, activity_id)
    if not act:
        raise HTTPException(status_code=404, detail="Activity not found")
    return act
