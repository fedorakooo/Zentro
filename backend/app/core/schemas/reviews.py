from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    user_id: int
    rating: conint(ge=1, le=5)  # Rating should be between 1 and 5
    comment: Optional[str] = None


# Shared properties for review, base class for common review attributes
class ProductReviewBase(ReviewBase):
    product_id: int
    created_at: datetime
    updated_at: datetime


# Properties to receive via API when creating a review
class ProductReviewCreate(ReviewBase):
    product_id: int


# Main Review model with all properties
class ProductReview(ProductReviewBase):
    id: int


class DistributionCentreReviewBase(ReviewBase):
    distribution_centre_id: int
    created_at: datetime
    updated_at: datetime


class DistributionCentreCreate(ReviewBase):
    distribution_centre_id: int


# Main Review model with all properties
class DistributionCentreReview(DistributionCentreReviewBase):
    id: int
