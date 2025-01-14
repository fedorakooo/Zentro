from datetime import datetime

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Numeric
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression

from app.core.db import Base


class Category(Base):
    __tablename__ = "categories"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name: str = Column(String(100), nullable=False, unique=True)
    parent_id: int = Column(Integer, ForeignKey("categories.id"), nullable=True)
    created_at: datetime = Column(DateTime, server_default=expression.func.now(), nullable=False)
    updated_at: datetime = Column(DateTime, server_default=expression.func.now(), nullable=False)


class Product(Base):
    __tablename__ = "products"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    manufacturer: str = Column(String(150), nullable=False)
    name: str = Column(String(150), nullable=False)
    description: str = Column(String(1000), nullable=True)
    attributes: dict = Column(JSON, nullable=True)
    price: float = Column(Numeric(precision=10, scale=2), nullable=False)
    seller_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id: int = Column(Integer, ForeignKey("categories.id"), nullable=False)
    quantity_in_stock: int = Column(Integer, default=0, nullable=False)
    image_url: str = Column(String(300), nullable=True)
    is_active: bool = Column(Boolean(), server_default="true", nullable=False)
    created_at: DateTime = Column(DateTime, server_default=expression.func.now(), nullable=False)
    updated_at: DateTime = Column(
        DateTime,
        server_default=expression.func.now(),
        onupdate=expression.func.now(),
        nullable=False
    )


class ProductSize(Base):
    __tablename__ = "product_sizes"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    product_id: int = Column(Integer, ForeignKey("products.id"), nullable=False)
    size: str = Column(String(50), nullable=False)
    quantity: int = Column(Integer, default=0, nullable=False)
    created_at: DateTime = Column(DateTime, server_default=expression.func.now(), nullable=False)
    updated_at: DateTime = Column(
        DateTime,
        server_default=expression.func.now(),
        onupdate=expression.func.now(),
        nullable=False
    )
