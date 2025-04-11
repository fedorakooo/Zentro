from src.application.abstractions.abstract_review_service import AbstractReviewService
from src.enums.review_status import ReviewStatus
from src.models.review import ReviewORM
from src.schemas.review import ReviewCreate, ReviewRead


class ReviewService(AbstractReviewService):
    def __init__(self, review_repository: AbstractReviewService):
        self.repository = review_repository

    async def get_product_reviews(
            self,
            product_id: str,
            rating: int | None,
            skip: int = 0,
            limit: int = 100
    ) -> list[ReviewRead]:
        reviews = await self.repository.get_product_reviews(
            product_id=product_id,
            rating=rating,
            skip=skip,
            limit=limit,
        )
        return [ReviewRead.from_orm(review) for review in reviews]

    async def create(
            self,
            review_create: ReviewCreate,
            user_id: int,
            product_id: int
    ) -> ReviewRead:
        review_orm = ReviewORM(
            **review_create.dict(),
            user_id=user_id,
            product_id=product_id,
            status=ReviewStatus.ACTIVE
        )

        review = await self.repository.create(review_orm)
        return ReviewRead.from_orm(review)
