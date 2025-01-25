from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.models.reviews import ProductReviewORM
from app.core.schemas.reviews import ProductReviewCreate
from app.dependencies.db import get_db


async def add_review_about_product(review: ProductReviewCreate):
    async with get_db() as db:
        try:
            query = select(ProductReviewORM).where(
                ProductReviewORM.user_id == review.user_id,
                ProductReviewORM.product_id == review.product_id
            )
            result = await db.execute(query)
            review_db = result.scalars().one_or_none()

            if review_db:
                raise HTTPException(
                    status_code=409,
                    detail="You have already submitted a review for this product"
                )

            new_review = ProductReviewORM(**review.dict())

            db.add(new_review)
            db.commit()
            db.refresh(review)

            return {
                "message": "Review added successfully"
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while fetching the product",
            )
