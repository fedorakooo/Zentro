from pydantic import BaseModel, conint
from datetime import datetime

from src.enums.review import ReviewStatus


class ReviewCreate(BaseModel):
    rating: conint(ge=1, le=5)
    comment: str | None


class ReviewRead(BaseModel):
    id: int
    user_id: int
    product_id: str
    rating: conint(ge=1, le=5)
    comment: str | None
    status: ReviewStatus
    updated_at: datetime
    created_at: datetime
