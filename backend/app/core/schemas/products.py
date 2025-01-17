from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# Shared properties for product, base class for common product attributes
class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    seller_id: int
    category_id: int
    quantity_in_stock: int
    image_url: str
    is_active: bool
    created_at: datetime
    updated_at: datetime


# Properties to receive via API when updating product details, all are optional
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None
    quantity_in_stock: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


# Properties to receive via API when creating a product
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    seller_id: int
    category_id: int
    quantity_in_stock: int
    image_url: str
    is_active: bool


# Main Product model with all properties
class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


class ProductSizeBase(BaseModel):
    product_id: int
    size: str
    quantity: int


class ProductSizeCreate(ProductSizeBase):
    pass


class ProductSizeUpdate(BaseModel):
    size: Optional[str] = None
    quantity: Optional[int] = None


class ProductSize(ProductSizeBase):
    id: int
    created_at: datetime
    updated_at: datetime
