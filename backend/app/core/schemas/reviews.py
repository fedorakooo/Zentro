from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional


# Shared properties for review, base class for common review attributes
class ReviewBase(BaseModel):
    user_id: int
    product_id: int
    rating: conint(ge=1, le=5)  # Rating should be between 1 and 5
    comment: Optional[str] = None
    created_at: datetime
    updated_at: datetime


# Properties to receive via API when updating review details, all are optional
class ReviewUpdate(BaseModel):
    rating: Optional[conint(ge=1, le=5)] = None
    comment: Optional[str] = None


# Properties to receive via API when creating a review
class ReviewCreate(BaseModel):
    user_id: int
    product_id: int
    rating: conint(ge=1, le=5)
    comment: Optional[str] = None


# Main Review model with all properties
class Review(ReviewBase):
    id: int
