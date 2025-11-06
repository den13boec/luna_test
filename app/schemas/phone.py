from pydantic import BaseModel, ConfigDict


class PhoneOut(BaseModel):
    id: int
    phone: str
    model_config = ConfigDict(from_attributes=True)
