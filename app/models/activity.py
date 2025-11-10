from __future__ import annotations
from datetime import datetime
from sqlalchemy import (
    String,
    SmallInteger,
    ForeignKey,
    DateTime,
    CheckConstraint,
    Index,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE"), nullable=True, index=True
    )
    depth: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    # self-referencing
    parent: Mapped["Activity | None"] = relationship(
        back_populates="children", remote_side=[id]
    )
    children: Mapped[list["Activity"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )

    __table_args__ = (
        # depth check constraint
        CheckConstraint("depth >= 1 AND depth <= 3", name="ck_activities_depth_1_3"),
        # uniqueness of a name within one parent (for a non-empty parent_id)
        Index(
            "uq_activity_parent_name",
            "parent_id",
            "name",
            unique=True,
            postgresql_where=text("parent_id IS NOT NULL"),
        ),
        # uniqueness of the name among roots (parent_id IS NULL)
        Index(
            "uq_activity_root_name",
            "name",
            unique=True,
            postgresql_where=text("parent_id IS NULL"),
        ),
    )
