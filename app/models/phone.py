from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey
from app.db.base import Base


class Phone(Base):
    __tablename__ = "phones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), index=True
    )
    phone: Mapped[str] = mapped_column(String(32), nullable=False, index=True)

    organization = relationship("Organization", back_populates="phones")
