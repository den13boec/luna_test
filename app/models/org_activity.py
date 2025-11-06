from sqlalchemy import Table, Column, Integer, ForeignKey, UniqueConstraint
from app.db.base import Base

org_activity = Table(
    "org_activity",
    Base.metadata,
    Column(
        "organization_id",
        Integer,
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "activity_id",
        Integer,
        ForeignKey("activities.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    UniqueConstraint("organization_id", "activity_id", name="uq_org_activity"),
)
