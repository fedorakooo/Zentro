from sqlalchemy import (
    Table, Column, Integer, String, Boolean, Float, Date, MetaData, ForeignKey
)
from sqlalchemy.sql import expression

metadata = MetaData()

products_table = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(150), nullable=False),
    Column("description", String(1000), nullable=True),
    Column("price", Float, nullable=False),
    Column("category", String(100), nullable=False),
    Column("quantity_in_stock", Integer, default=0, nullable=False),
    Column("image_url", String(300), nullable=True),
    Column("is_active", Boolean(), server_default="true", nullable=False),
    Column("created_at", Date, server_default=expression.func.now(), nullable=False),
    Column("updated_at", Date, server_default=expression.func.now(), onupdate=expression.func.now(), nullable=False),
)
