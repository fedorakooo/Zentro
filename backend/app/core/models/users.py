from sqlalchemy import (
    Table, Column, String, Boolean, Float, DateTime, ForeignKey, MetaData, Integer
)
from sqlalchemy.sql import expression

metadata = MetaData()

users_table = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("email", String(100), unique=True, index=True, nullable=True),
    Column("name", String(150), nullable=False),
    Column("hashed_password", String(), nullable=False),
    Column("phone_number", String(20), unique=True, index=True, nullable=False),
    Column("is_active", Boolean(), server_default=expression.true(), nullable=False),
    Column("is_seller", Boolean(), server_default=expression.false(), nullable=False),
    Column("balance", Float, server_default="0.0", nullable=False),
    Column("registration_date", DateTime, server_default=expression.func.now(), nullable=False),
    Column("address", String(300), nullable=True),
    Column("loyalty_points", Float, server_default="0.0", nullable=False),
    Column("profile_picture_url", String(300), nullable=True),
    Column("referral_code", String(50), unique=True, nullable=True),
    Column("gender", String(1), nullable=True)
)

saved_cards_table = Table(
    "saved_cards",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey(users_table.c.id), nullable=False),
    Column("card_number", String(4), nullable=False),
    Column("card_type", String(50), nullable=False),
    Column("expiry_date", DateTime, nullable=False),
    Column("is_default", Boolean(), server_default="false", nullable=False),
    Column("card_holder_name", String(150), nullable=False),
)
