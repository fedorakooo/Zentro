from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class DistributionCentreBase(BaseModel):
    address: str
    start_time: datetime
    end_time: datetime
    contact_info: Optional[str] = None


class DistributionCenterCreate(DistributionCentreBase):
    owner_id: int


class DistributionCentre(DistributionCentreBase):
    average_rating: float
    rating_count: int