from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DistributionCenterBase(BaseModel):
    address: str
    start_time: datetime
    end_time: datetime
    contact_info: Optional[str] = None


class DistributionCenterCreate(DistributionCenterBase):
    owner_id: int


class DistributionCenter(DistributionCenterBase):
    average_rating: float
    rating_count: int

    class Config:
        from_attributes = True
