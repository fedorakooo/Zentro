from sqlalchemy import select

from app.core.schemas.cart import CartItemRequest
from app.core.models.cart import CartORM
from app.dependencies.db import get_db


async def get_cart_product_id_by_user_id(user_id: int):
    async with get_db() as db:
        query = select(CartORM).where(CartORM.user_id == user_id)
        result = await db.execute(query)
        products_db = result.scalars().all()

    products = []
    for product_db in products_db:
        products.append(CartItemRequest.from_orm(product_db))
    return products
