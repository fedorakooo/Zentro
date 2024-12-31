from pydantic import BaseModel, EmailStr, condecimal, constr
from datetime import date
from typing import Optional


# Shared properties for user, base class for common user attributes
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    name: str
    phone_number: constr(regex=r"^\+?\d{1,3}?[-.\s]?\(?\d+\)?[-.\s]?\d+[-.\s]?\d+$")
    is_active: bool = True
    is_seller: bool = False
    balance: condecimal(max_digits=10, decimal_places=2) = 0.0
    registration_date: date
    address: Optional[str] = None
    loyalty_points: condecimal(max_digits=10, decimal_places=2) = 0.0
    profile_picture_url: Optional[str] = None
    referral_code: Optional[str] = None
    gender: Optional[str] = None


# Properties to receive via API when creating a user
class UserCreate(UserBase):
    hashed_password: str


# Properties to receive via API when updating user details, all are optional
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = None
    is_seller: Optional[bool] = None
    balance: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    address: Optional[str] = None
    loyalty_points: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    profile_picture_url: Optional[str] = None
    referral_code: Optional[str] = None
    gender: Optional[str] = None


# Properties for updating user password
class UpdatePassword(BaseModel):
    old_password: str
    new_password: str


# Main User model with all properties
class User(UserBase):
    id: int
    registration_date: date


# Shared properties for saved credit card
class SavedCardBase(BaseModel):
    card_number: str
    card_type: str
    expiry_date: date
    card_holder_name: str
    is_default: bool = False


# Main Saved card model with all properties
class SavedCard(SavedCardBase):
    id: int
    user_id: int