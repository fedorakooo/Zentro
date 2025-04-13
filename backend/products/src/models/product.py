from datetime import datetime, timezone
from beanie import Document, PydanticObjectId
from pydantic import Field

from src.core.enums.product import ProductStatus
from src.schemas.products import ProductVariantSchema


class Product(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias="_id")
    name: str
    brand: str
    brand_id: int
    supplier_id: int
    average_rating: float = 0
    review_count: int = 0
    price: float | None = None
    quantity: int | None = None
    category_id: int
    status: ProductStatus
    variants: list[ProductVariantSchema] | None = None
    photos: list[str] | None = None
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "products"
        indexes = [
            "brand_id",
            "supplier_id",
            "category_id",
            ["brand_id", "category_id"],
            "price",
            [("name", "text"), ("brand", "text")]
        ]

    class Config:
        json_encoders = {
            PydanticObjectId: str,
            ProductVariantSchema: lambda v: v.dict()
        }
        from_attributes = True
        validate_by_name = True
