from typing import List

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.models.products import ProductORM
from app.core.schemas.cart import CartItemDTO, CartItem
from app.core.models.cart import CartORM
from app.core.schemas.products import Product
from app.dependencies.db import get_db


async def get_cart_products_by_user_id(user_id: int) -> List[Product]:
    # Receive data about products in the basket
    products_data: List[CartItemDTO] = await get_cart_product_data_object_by_user_id(user_id)

    # If the cart is empty, return an empty list
    if not products_data:
        return []

    product_ids = [product_data.product_id for product_data in products_data]

    async with get_db() as db:
        try:
            query = select(ProductORM).where(ProductORM.id.in_(product_ids))
            result = await db.execute(query)
            products_db = {product.id: product for product in result.scalars().all()}

            cart_items = []

            for product_data in products_data:
                product_db = products_db.get(product_data.product_id)

                if not product_db:
                    # If the product is not found in the database, return an error
                    raise HTTPException(
                        status_code=404,
                        detail=f"Product with ID {product_data.product_id} not found"
                    )

                product = Product.from_orm(product_db)
                cart_item = CartItem(**product.dict(), quantity=product_data.quantity)
                cart_items.append(cart_item)

            return cart_items

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while fetching the product",
            )


async def get_cart_product_data_object_by_user_id(user_id: int) -> List[CartItemDTO]:
    async with get_db() as db:
        try:
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

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while fetching the product",
            )
