from sqlalchemy import (
    Table, Column, Integer, String, Boolean, Float, DateTime, MetaData, ForeignKey, JSON
)
from sqlalchemy.sql import expression

metadata = MetaData()

categories_table = Table(
    "categories",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False, unique=True),
    Column("parent_id", Integer, ForeignKey("categories.id"), nullable=True),
    Column("created_at", DateTime, server_default=expression.func.now(), nullable=False),
    Column("updated_at", DateTime, server_default=expression.func.now(), onupdate=expression.func.now(), nullable=False),
)

products_table = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("manufacturer", String(150), nullable=False),
    Column("name", String(150), nullable=False),
    Column("description", String(1000), nullable=True),
    Column("attributes", JSON, nullable=True),
    Column("price", Float, nullable=False),
    Column("category_id", Integer, ForeignKey(categories_table.c.id), nullable=False),
    Column("quantity_in_stock", Integer, default=0, nullable=False),
    Column("image_url", String(300), nullable=True),
    Column("is_active", Boolean(), server_default="true", nullable=False),
    Column("created_at", DateTime, server_default=expression.func.now(), nullable=False),
    Column("updated_at", DateTime, server_default=expression.func.now(), onupdate=expression.func.now(), nullable=False),
)

product_sizes_table = Table(
    "product_sizes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("product_id", Integer, ForeignKey(products_table.c.id), nullable=False),
    Column("size", String(50), nullable=False),
    Column("quantity", Integer, default=0, nullable=False),
    Column("created_at", DateTime, server_default=expression.func.now(), nullable=False),
    Column("updated_at", DateTime, server_default=expression.func.now(), onupdate=expression.func.now(), nullable=False),
)
