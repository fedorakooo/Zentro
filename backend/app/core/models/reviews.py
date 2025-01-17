from sqlalchemy import (
    Column, Integer, String, ForeignKey
)
from sqlalchemy.orm import mapped_column, Mapped

from app.core.db import Base


class ReviewORM(Base):
    __tablename__ = "reviews"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    product_id: Mapped[int] = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating: Mapped[int] = Column(Integer, nullable=False)
    comment: Mapped[str] = Column(String(1000), nullable=True)
