from typing import List

from sqlalchemy import select

from app.core.models.products import ProductORM
from app.core.schemas.cart import CartItemDTO, CartItem
from app.core.models.cart import CartORM
from app.core.schemas.products import Product
from app.dependencies.db import get_db


async def get_cart_products_by_user_id(user_id: int) -> List[Product]:
    products_data: List[CartItemDTO] = await get_cart_product_data_object_by_user_id(user_id)

    cart_items: List[CartItem] = []

    async with get_db() as db:
        for product_data in products_data:
            query = select(ProductORM).where(ProductORM.id == product_data.product_id)
            result = await db.execute(query)
            product_db = result.scalars().one_or_none()

            product = Product.from_orm(product_db)

            cart_item = CartItem(**product.dict(), quantity=product_data.quantity)

            cart_items.append(cart_item)

    return cart_items


async def get_cart_product_data_object_by_user_id(user_id: int) -> List[CartItemDTO]:
    async with get_db() as db:
        query = select(CartORM).where(CartORM.user_id == user_id)
        result = await db.execute(query)
        products_db = result.scalars().all()

        return [
            CartItemDTO(
                product_id=product_db.product_id,
                quantity=product_db.quantity
            )
            for product_db in products_db
        ]

