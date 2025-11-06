from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Building(Base):
    __tablename__ = "buildings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    longitude: Mapped[float] = mapped_column(Float, nullable=False, index=True)
    created_at: Mapped = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    organizations = relationship(
        "Organization", back_populates="building", cascade="all,delete"
    )
