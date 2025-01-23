from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.models.cart import CartORM
from app.core.models.products import ProductORM
from app.core.schemas.cart import CartItemRequest
from app.core.schemas.products import Product, ProductCreateDB
from app.dependencies.db import get_db


async def get_product_by_id(product_id: int) -> Product:
    async with get_db() as db:
        try:
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

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while fetching the product",
            )


async def add_item_to_cart(cart_item: CartItemRequest):
    if cart_item.quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="Quantity must be greater than zero"
        )

    async with get_db() as db:
        try:
            query = select(CartORM).where(
                CartORM.user_id == cart_item.user_id,
                CartORM.product_id == cart_item.product_id
            )
            result = await db.execute(query)
            cart_item_db = result.scalars().one_or_none()

            if cart_item_db:
                cart_item_db.quantity += cart_item.quantity
                await db.commit()
                return {
                    "message": "Product quantity updated successfully"
                }

            new_cart_item = CartORM(**cart_item.dict())

            db.add(new_cart_item)
            await db.commit()
            await db.refresh(new_cart_item)

            return {
                "message": "Product added to cart successfully"
            }

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Failed to add product due to a database error"
            )


async def add_new_product(product: ProductCreateDB):
    async with get_db() as db:
        try:
            new_product = ProductORM(**product.dict())
            print(new_product.id)

            db.add(new_product)
            await db.commit()
            await db.refresh(new_product)

            return {
                "message": "New product added successfully",
                "product_id": new_product.id
            }

        except SQLAlchemyError as e:
            await db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Failed to add product due to a database error"
            )
