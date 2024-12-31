from sqlalchemy import (
    Table, Column, Integer, String, Date, MetaData, ForeignKey
)
from sqlalchemy.sql import expression

from app.core.models.users import users_table
from app.core.models.products import products_table

metadata = MetaData()

reviews_table = Table(
    "reviews",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, ForeignKey(users_table.c.id), nullable=False),
    Column("product_id", Integer, ForeignKey(products_table.c.id), nullable=False),
    Column("rating", Integer, nullable=False),
    Column("comment", String(1000), nullable=True),
    Column("created_at", Date, server_default=expression.func.now(), nullable=False),
    Column("updated_at", Date, server_default=expression.func.now(), onupdate=expression.func.now(), nullable=False)
)
