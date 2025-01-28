from pydantic import BaseModel, EmailStr, condecimal
from datetime import datetime
from typing import Optional

from app.core.emuns.user import UserRole


# Shared properties for user, base class for common user attributes
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    name: str
    phone_number: str
    is_active: bool = True
    role: UserRole
    balance: condecimal(max_digits=10, decimal_places=2) = 0.0
    created_at: datetime
    updated_at: datetime
    address: Optional[str] = None
    loyalty_points: condecimal(max_digits=10, decimal_places=2) = 0.0
    profile_picture_url: Optional[str] = None
    referral_code: Optional[str] = None
    gender: Optional[str] = None


# Properties to receive via API when updating user details, all are optional
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    profile_picture_url: Optional[str] = None
    gender: Optional[str] = None


# Properties for updating user password
class UpdatePassword(BaseModel):
    old_password: str
    new_password: str


# Main User model with all properties
class User(UserBase):
    id: int

    class Config:
        from_attributes = True


# Properties to receive via API when creating a user
class UserRegisterRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone_number: str
    name: str
    password: str
    role: UserRole


class UserLoginRequest(BaseModel):
    phone_number: str
    password: str


# Shared properties for saved credit card
class SavedCardBase(BaseModel):
    card_number: str
    card_type: str
    created_at: datetime
    updated_at: datetime
    card_holder_name: str
    is_default: bool = False


# Main Saved card model with all properties
class SavedCard(SavedCardBase):
    id: int
    user_id: int
