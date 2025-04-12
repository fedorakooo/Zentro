from pydantic import BaseModel
from enum import Enum


class ProductEventType(str, Enum):
    DELETE = "DELETE"
    DELETE_COMPENSATE = "DELETE_COMPENSATE"


class ProductEvent(BaseModel):
    event_id: str
    type: ProductEventType
    product_id: str
    original_status: str | None = None
    timestamp: int
