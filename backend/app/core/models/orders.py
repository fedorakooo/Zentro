from sqlalchemy import (
    Column, String, DateTime, ForeignKey, Integer, Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.core.db import Base


class Order(Base):
    __tablename__ = 'orders'

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    order_date: str = Column(DateTime, server_default=expression.func.now(), nullable=False)
    total_amount: float = Column(Numeric(precision=10, scale=2), nullable=False)
    status: str = Column(String(50), nullable=False)
    shipping_address: str = Column(String(300), nullable=False)
    payment_method: str = Column(String(50), nullable=False)


class OrderProduct(Base):
    __tablename__ = "order_products"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    order_id: int = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity: int = Column(Integer, nullable=False)
