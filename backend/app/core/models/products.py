from sqlalchemy import (
    Boolean, ForeignKey, JSON, Numeric, String, Integer
)
from sqlalchemy.orm import mapped_column, Mapped

from app.core.db import Base


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=True)


class Product(Base):
    __tablename__ = "products"

    manufacturer: Mapped[str] = mapped_column(String(150), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=True)
    attributes: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), nullable=False)
    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    image_url: Mapped[str] = mapped_column(String(300), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), server_default="true", nullable=False)


class ProductSize(Base):
    __tablename__ = "product_sizes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    size: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
