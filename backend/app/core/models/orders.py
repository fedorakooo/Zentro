from sqlalchemy import (
    Table, Column, String, Float, DateTime, ForeignKey, MetaData, Integer
)
from sqlalchemy.sql import expression

from app.core.models.users import users_table
from app.core.models.products import products_table

metadata = MetaData()

orders_table = Table(
    "orders",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey(users_table.c.id), nullable=False),
    Column("order_date", DateTime, server_default=expression.func.now(), nullable=False),
    Column("total_amount", Float, nullable=False),
    Column("status", String(50), nullable=False),
    Column("shipping_address", String(300), nullable=True),
    Column("payment_method", String(50), nullable=True)
)

order_products_table = Table(
    "order_products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("order_id", Integer, ForeignKey(orders_table.c.id), nullable=False),
    Column("product_id", Integer, ForeignKey(products_table.c.id), nullable=False),
    Column("quantity", Integer, nullable=False),
    Column("price_per_unit", Float, nullable=False)
)
