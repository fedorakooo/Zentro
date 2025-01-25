from sqlalchemy import (
    Integer, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class CartORM(Base):
    __tablename__ = "cart"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
