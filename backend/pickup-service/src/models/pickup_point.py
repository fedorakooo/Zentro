from datetime import datetime

from pydantic import BaseModel, EmailStr

from src.core.enums.pickup_point import PickupPointStatus


class PickupPointResponse(BaseModel):
    id: int
    owner_id: int
    address: str
    latitude: float
    longitude: float
    working_hours: str
    status: PickupPointStatus
    phone: str | None
    email: EmailStr | None
    description: str | None
    created_at: datetime
    updated_at: datetime


class PickupPointCreateRequest(BaseModel):
    address: str
    latitude: float
    longitude: float
    working_hours: str
    phone: str | None = None
    email: EmailStr | None = None
    description: str | None = None
