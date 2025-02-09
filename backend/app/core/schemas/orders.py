from pydantic import BaseModel, condecimal
from datetime import datetime
from typing import Optional


# Shared properties for order, base class for common order attributes
class OrderBase(BaseModel):
    user_id: int
    created_at: datetime
    updated_at: datetime
    total_amount: condecimal(gt=0)  # Ensure total amount is greater than zero
    status: str
    distribution_center_id: int
    payment_method: Optional[str] = None


# Properties to receive via API when updating order details, all are optional
class OrderUpdate(BaseModel):
    status: Optional[str] = None
    distribution_center_id: int
    payment_method: Optional[str] = None


# Properties to receive via API when creating an order
class OrderCreate(BaseModel):
    user_id: int
    total_amount: condecimal(gt=0)  # Ensure total amount is greater than zero
    status: str
    distribution_center_id: int
    payment_method: Optional[str] = None


# Main Order model with all properties
class Order(OrderBase):
    id: int


# OrderProduct model (to represent the relation between orders and products)
class OrderProductBase(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_per_unit: condecimal(gt=0)  # Ensure price per unit is greater than zero


# Properties to receive via API when creating an order-product relation
class OrderProductCreate(OrderProductBase):
    pass


# Main OrderProduct model with all properties
class OrderProduct(OrderProductBase):
    id: int
