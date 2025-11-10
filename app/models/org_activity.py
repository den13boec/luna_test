from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint
from app.db.base import Base

org_activity = Table(
    "org_activity",
    Base.metadata,
    Column(
        "organization_id",
        ForeignKey("organizations.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "activity_id", ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True
    ),
    # PK ensures the uniqueness of the pair, but leave explicit UC for readability
    UniqueConstraint("organization_id", "activity_id", name="uq_org_activity"),
)
