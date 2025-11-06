from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    SmallInteger,
    CheckConstraint,
    UniqueConstraint,
    DateTime,
)
from sqlalchemy.sql import func
from app.db.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("activities.id", ondelete="SET NULL"), nullable=True, index=True
    )
    depth: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)  # 1..3
    created_at: Mapped = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    parent = relationship("Activity", remote_side=[id], backref="children")

    __table_args__ = (
        CheckConstraint("depth >= 1 AND depth <= 3", name="ck_activities_depth_1_3"),
        UniqueConstraint("parent_id", "name", name="uq_activity_parent_name"),
    )
