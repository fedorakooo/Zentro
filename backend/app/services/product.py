from fastapi import HTTPException

from sqlalchemy import select

from app.core.models.products import ProductORM
from app.core.schemas.products import Product
from app.dependencies.db import get_db


async def get_product_by_id(product_id: int) -> Product:
    async with get_db() as db:
        query = select(ProductORM).where(ProductORM.id == product_id)
        result = await db.execute(query)

    product_db = result.scalars().one_or_none()

    if not product_db:
        raise HTTPException(status_code=404, detail="Product not found")

    product = Product.from_orm(product_db)

    return product