from sqlalchemy import (
    String, Boolean, ForeignKey, Integer, Numeric
)
from sqlalchemy.orm import mapped_column, Mapped

from app.core.db import Base


class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_seller: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), default=0.0, nullable=False)
    address: Mapped[str] = mapped_column(String(300), nullable=True)
    loyalty_points: Mapped[float] = mapped_column(Numeric(precision=10, scale=2), default="0.0", nullable=False)
    profile_picture_url: Mapped[str] = mapped_column(String(300), nullable=True)
    referral_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)
    gender: Mapped[str] = mapped_column(String(1), nullable=True)


class SavedCard(Base):
    __tablename__ = "saved_cards"

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    card_number: Mapped[str] = mapped_column(String(4), nullable=False)  # The last 4 digits of the card
    card_type: Mapped[str] = mapped_column(String(50), nullable=False)
    is_default: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)
    card_holder_name: Mapped[str] = mapped_column(String(150), nullable=False)
