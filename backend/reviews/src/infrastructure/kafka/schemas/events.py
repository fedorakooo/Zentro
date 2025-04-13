from pydantic import BaseModel
from enum import Enum


class ReviewEventType(str, Enum):
    DELETE = "DELETE"
    DELETE_COMPENSATE = "DELETE_COMPENSATE"


class ReviewEvent(BaseModel):
    event_id: str
    type: ReviewEventType
    review_id: int
    original_status: str | None = None
    timestamp: int