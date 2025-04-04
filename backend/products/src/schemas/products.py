from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from beanie import PydanticObjectId


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
    id: PydanticObjectId = Field(..., alias="_id")
    price: float | None = None
    quantity: int | None = None
    variants: list[ProductVariantSchema] | None = None
    photos: list[str] | None = None
    updated_at: datetime | None = None
    created_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        json_encoders={
            PydanticObjectId: str
        }
    )