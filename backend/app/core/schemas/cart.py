from pydantic import BaseModel

from app.core.schemas.products import Product


class CartItemRequest(BaseModel):
    product_id: int
    quantity: int
    user_id: int


class CartItemDTO(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class CartItem(Product):
    quantity: int
