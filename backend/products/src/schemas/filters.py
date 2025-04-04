from pydantic import BaseModel


class ProductFilter(BaseModel):
    name: str | None = None
    brand: str | None = None
    brand_id: int | None = None
    category_id: int | None = None
    min_price: float | None = None
    max_price: float | None = None
