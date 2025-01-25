from sqlalchemy import (
    String, ForeignKey, Integer, DateTime, Numeric, Boolean
)
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.core.db import Base


class DistributionCenterORM(Base):
    __tablename__ = "distribution_centers"

    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    start_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_time: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    average_rating: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), default=0.0)
    rating_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    contact_info: Mapped[str] = mapped_column(String(100), nullable=True)
