from pydantic import BaseModel, ConfigDict
from typing import List
from app.schemas.building import BuildingOut
from app.schemas.phone import PhoneOut
from app.schemas.activity import ActivityOut


class OrganizationBase(BaseModel):
    name: str
    building_id: int


class OrganizationOut(OrganizationBase):
    id: int
    building: BuildingOut
    phones: List[PhoneOut]
    activities: List[ActivityOut]
    model_config = ConfigDict(from_attributes=True)
