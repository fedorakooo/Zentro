from datetime import datetime

from pydantic import BaseModel, EmailStr


class PickupPointOperatorResponse(BaseModel):
    id: int
    pickup_point_id: int
    name: str
    email: EmailStr
    phone_number: str
    password: str
    created_at: datetime
    updated_at: datetime


class PickupPointOperatorCreateRequest(BaseModel):
    pickup_point_id: int
    name: str
    email: EmailStr
    phone_number: str
    password: str
