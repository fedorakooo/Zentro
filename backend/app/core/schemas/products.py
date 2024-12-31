from typing import Optional

from pydantic import BaseModel
from datetime import date


# Shared properties for product, base class for common product attributes
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    quantity_in_stock: int
    image_url: str
    is_active: bool
    created_at: date
    updated_at: date


# Properties to receive via API when updating product details, all are optional
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    quantity_in_stock: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


# Properties to receive via API when creating a product
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    quantity_in_stock: int
    image_url: str
    is_active: bool


# Main Product model with all properties
class Product(ProductBase):
    id: int
