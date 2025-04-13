from datetime import datetime
from pydantic import BaseModel, validator
from beanie import PydanticObjectId

from src.core.enums.product import ProductStatus


class ProductVariantSchema(BaseModel):
    criterion: str
    value: str
    price: float
    quantity: int
    description: str | None = None


class ProductBase(BaseModel):
    name: str
    brand: str
    brand_id: int
    supplier_id: int
    category_id: int


class ProductCreate(ProductBase):
    price: float | None = None
    quantity: int | None = None
    variants: list[ProductVariantSchema] | None = None
    photos: list[str] | None = None


class ProductUpdate(ProductBase):
    name: str | None = None
    brand: str | None = None
    brand_id: int | None = None
    supplier_id: int | None = None
    category_id: int | None = None
    price: float | None = None
    quantity: int | None = None
    variants: list[ProductVariantSchema] | None = None
    photos: list[str] | None = None


class ProductRead(ProductBase):
    id: str
    price: float | None = None
    quantity: int | None = None
    variants: list[ProductVariantSchema] | None = None
    photos: list[str] | None = None
    status: ProductStatus
    updated_at: datetime
    created_at: datetime
    average_rating: float
    review_count: int

    @validator('id', pre=True)
    def convert_id_to_str(cls, value):
        if isinstance(value, PydanticObjectId):
            return str(value)
        return value

    class Config:
        from_attributes = True
