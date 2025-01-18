from pydantic import BaseModel


class CartItemRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int

    class Config:
        orm_mode = True
        from_attributes = True