from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.models.review import ReviewORM
from src.repositories.abstractions.abstract_review_repository import AbstractReviewRepository


class ReviewPostgreRepository(AbstractReviewRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def get_product_reviews(
            self,
            product_id: str,
            rating: int | None,
            skip: int = 0,
            limit: int = 100
    ) -> list[ReviewORM]:
        async with self.session_factory() as session:
            stmt = select(ReviewORM).where(ReviewORM.product_id == product_id)
            if rating is not None:
                stmt = stmt.where(ReviewORM.rating == rating)
            stmt = stmt.offset(skip).limit(limit)
            result = await session.execute(stmt)
            reviews = result.scalars().all()
            return reviews

    async def create(self, review: ReviewORM) -> ReviewORM:
        async with self.session_factory() as session:
            session.add(review)
            await session.commit()
            await session.refresh(review)
            return review
