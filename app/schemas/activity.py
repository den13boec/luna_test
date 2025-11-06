from __future__ import annotations
from pydantic import BaseModel, Field, ConfigDict


class ActivityBase(BaseModel):
    name: str
    parent_id: int | None = None


class ActivityOut(BaseModel):
    id: int
    name: str
    parent_id: int | None
    depth: int
    model_config = ConfigDict(from_attributes=True)


class ActivityTree(ActivityOut):
    children: list[ActivityTree] = Field(default_factory=list)


ActivityTree.model_rebuild()
