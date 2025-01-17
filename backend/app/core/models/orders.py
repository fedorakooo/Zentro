from sqlalchemy import (
    String, ForeignKey, Numeric, Integer
)
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class OrderORM(Base):
    __tablename__ = "orders"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_amount: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    shipping_address: Mapped[str] = mapped_column(String(300), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)


class OrderProductORM(Base):
    __tablename__ = "order_products"

    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
