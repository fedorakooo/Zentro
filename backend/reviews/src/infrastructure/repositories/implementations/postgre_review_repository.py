from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.enums.review_status import ReviewStatus
from src.models.review import ReviewORM
from src.infrastructure.repositories.abstractions.abstract_review_repository import AbstractReviewRepository


class ReviewPostgreRepository(AbstractReviewRepository):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory

    async def get_review_by_id(self, review_id: int) -> ReviewORM:
        async with self.session_factory() as session:
            stmt = select(ReviewORM).where(ReviewORM.id == review_id)
            result = await session.execute(stmt)
            review = result.scalar_one_or_none()
            return review

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

    async def create_review(self, review: ReviewORM) -> ReviewORM:
        async with self.session_factory() as session:
            session.add(review)
            await session.commit()
            await session.refresh(review)
            return review

    async def change_review_status(self, review_id: int, original_status: ReviewStatus) -> None:
        async with self.session_factory() as session:
            review = await self.get_review_by_id(review_id)
            if not review:
                raise ValueError()
            stmt = update(ReviewORM).where(ReviewORM.id == review.id).values(status=original_status)
            await session.execute(stmt)
            await session.commit()

    async def delete_review_by_id(self, review_id: str) -> None:
        async with self.session_factory() as session:
            stmt = update(ReviewORM).where(ReviewORM.id == review_id).values(status=ReviewStatus.DELETED)
            await session.execute(stmt)
            await session.commit()

    async def delete_reviews_by_product_id(self, product_id: str) -> None:
        async with self.session_factory() as session:
            stmt = update(ReviewORM).where(ReviewORM.product_id == product_id).values(status=ReviewStatus.DELETED)
            await session.execute(stmt)
            await session.commit()
