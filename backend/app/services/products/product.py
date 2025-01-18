from fastapi import HTTPException

from sqlalchemy import select

from app.core.models.cart import CartORM
from app.core.models.products import ProductORM
from app.core.schemas.cart import CartItemRequest
from app.core.schemas.products import Product
from app.dependencies.db import get_db


async def get_product_by_id(product_id: int) -> Product:
    async with get_db() as db:
        query = select(ProductORM).where(ProductORM.id == product_id)
        result = await db.execute(query)

    product_db = result.scalars().one_or_none()

    if not product_db:
        raise HTTPException(
            status_code=404,
            detail="Product not found"
        )

    product = Product.from_orm(product_db)

    return product


async def add_item_to_cart(cart_item: CartItemRequest):
    async with get_db() as db:
        query = select(CartORM).where(
            CartORM.user_id == cart_item.user_id,
            CartORM.product_id == cart_item.product_id
        )
        result = await db.execute(query)

        cart_item_db = result.scalars().one_or_none()

        if cart_item_db:
            cart_item_db.quantity += cart_item.quantity
            return {
                "message": "Product added to cart successfully"
            }

        new_cart_item = CartORM(**cart_item.dict())

        db.add(new_cart_item)
        db.commit()
        db.refresh(new_cart_item)

        return {
            "message": "Product added to cart successfully"
        }
