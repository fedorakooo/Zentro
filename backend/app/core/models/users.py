from sqlalchemy import (
    Column, String, Boolean, DateTime, ForeignKey, Integer, Numeric
)
from sqlalchemy.sql import expression

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    email: str = Column(String(100), unique=True, index=True, nullable=True)
    name: str = Column(String(150), nullable=False)
    hashed_password: str = Column(String, nullable=False)
    phone_number: str = Column(String(20), unique=True, index=True, nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_seller: bool = Column(Boolean, default=False, nullable=False)
    balance: float = Column(Numeric(precision=10, scale=2), default=0.0, nullable=False)
    registration_date: DateTime = Column(DateTime, server_default=expression.func.now(), nullable=False)
    address: str = Column(String(300), nullable=True)
    loyalty_points: float = Column(Numeric(precision=10, scale=2), default="0.0", nullable=False)
    profile_picture_url: str = Column(String(300), nullable=True)
    referral_code: str = Column(String(50), unique=True, nullable=True)
    gender: str = Column(String(1), nullable=True)


class SavedCard(Base):
    __tablename__ = "saved_cards"

    id: int = Column(Integer, primary_key=True, autoincrement=True)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    card_number: str = Column(String(4), nullable=False)  # The last 4 digits of the card
    card_type: str = Column(String(50), nullable=False)
    expiry_date: DateTime = Column(DateTime, nullable=False)
    is_default: bool = Column(Boolean, server_default="false", nullable=False)
    card_holder_name: str = Column(String(150), nullable=False)
