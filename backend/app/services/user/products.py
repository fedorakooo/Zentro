from fastapi import HTTPException
from sqlalchemy import select
from typing import List

from sqlalchemy.exc import SQLAlchemyError

from app.core.models.products import ProductORM
from app.core.schemas.products import Product
from app.dependencies.db import get_db


async def get_created_products_by_user_id(user_id) -> List[Product]:
    async with get_db() as db:
        try:
            query = select(ProductORM).where(ProductORM.seller_id == user_id)
            result = await db.execute(query)
            products_db = result.scalars().all()

            products = [Product.from_orm(product_db) for product_db in products_db]

            return products

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail="Failed to retrieve products due to a database error"
            )
