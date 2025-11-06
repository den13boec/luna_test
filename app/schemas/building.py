from pydantic import BaseModel, Field, ConfigDict


class BuildingBase(BaseModel):
    address: str = Field(..., examples=["г. Москва, ул. Ленина 1, офис 3"])
    latitude: float
    longitude: float


class BuildingOut(BuildingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
