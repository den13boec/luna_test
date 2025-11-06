from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
from app.models.org_activity import org_activity


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    building_id: Mapped[int] = mapped_column(
        ForeignKey("buildings.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    building = relationship("Building", back_populates="organizations")
    phones = relationship(
        "Phone", back_populates="organization", cascade="all,delete-orphan"
    )
    activities = relationship(
        "Activity", secondary=org_activity, backref="organizations"
    )
