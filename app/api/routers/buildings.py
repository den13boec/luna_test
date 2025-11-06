from typing import Sequence
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.security import get_api_key
from app.db.session import get_db
from app.crud.buildings import list_buildings
from app.models.building import Building
from app.schemas.building import BuildingOut

router = APIRouter(
    prefix="/buildings", tags=["buildings"], dependencies=[Depends(get_api_key)]
)


@router.get("", response_model=list[BuildingOut])
def get_buildings(db: Session = Depends(get_db)) -> Sequence[Building]:
    return list_buildings(db)
