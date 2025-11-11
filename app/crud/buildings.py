from typing import Sequence
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.building import Building


def list_buildings(db: Session) -> Sequence[Building]:
    """Все здания (справочник)."""
    return db.execute(select(Building).order_by(Building.id)).scalars().all()
