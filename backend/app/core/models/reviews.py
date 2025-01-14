from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey
)
from sqlalchemy.sql import expression

from app.core.db import Base


class Review(Base):
    __tablename__ = "reviews"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
    rating: int = Column(Integer, nullable=False)
    comment: str = Column(String(1000), nullable=True)
    created_at: DateTime = Column(DateTime, server_default=expression.func.now(), nullable=False)
    updated_at: DateTime = Column(
        DateTime,
        server_default=expression.func.now(),
        onupdate=expression.func.now(),
        nullable=False
    )
