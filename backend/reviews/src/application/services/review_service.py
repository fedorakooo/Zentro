from src.application.abstractions.abstract_review_service import AbstractReviewService
from src.enums.review_status import ReviewStatus
from src.infrastructure.repositories.abstractions.abstract_review_repository import AbstractReviewRepository
from src.infrastructure.kafka.producers.producer import Producer
from src.models.review import ReviewORM
from src.schemas.review import ReviewCreate, ReviewRead
from src.schemas.saga import SagaResponse


class ReviewService(AbstractReviewService):
    def __init__(
            self,
            review_repository: AbstractReviewRepository,
            producer: Producer
    ):
        self.repository = review_repository
        self.producer = producer

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

    async def create_review(
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

        review = await self.repository.create_review(review_orm)
        return ReviewRead.from_orm(review)

    async def delete_review_by_id(self, review_id: int) -> SagaResponse:
        review = await self.repository.get_review_by_id(review_id)

        await self.producer.start()

        await self.producer.send_delete_event(
            review_id=review_id,
            original_status=review.status
        )

        await self.producer.stop()

        await self.repository.delete_review_by_id(review_id)

        return SagaResponse(
            success=True,
            message="Review deletion started",
            compensation_data={
                "review_id": review_id,
                "original_status": review.status
            }
        )

    async def compensate_delete_review(self, review_id: int, original_status: ReviewStatus) -> bool:
        await self.producer.start()

        await self.producer.send_compensation_event(
            review_id=review_id
        )

        await self.producer.stop()

        await self.repository.change_review_status(review_id, original_status)

        return SagaResponse(
            success=True,
            message="Review compensation started",
            compensation_data={
                "review_id": review_id
            }
        )

    async def delete_all_reviews_by_product_id(self, product_id: str) -> None:
        await self.repository.delete_reviews_by_product_id(product_id)
