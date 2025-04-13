from abc import ABC, abstractmethod

from src.enums.review_status import ReviewStatus
from src.schemas.review import ReviewCreate, ReviewRead


class AbstractReviewService(ABC):
    @abstractmethod
    async def get_product_reviews(
            self,
            product_id: str,
            rating: int | None,
            skip: int = 0,
            limit: int = 100
    ) -> list[ReviewRead]:
        pass

    @abstractmethod
    async def create_review(self, review: ReviewCreate, user_id: int, product_id: str) -> ReviewRead:
        pass

    @abstractmethod
    async def delete_review_by_id(self, review_id: int) -> bool:
        pass

    @abstractmethod
    async def compensate_delete_review(self, review_id: int, original_status: ReviewStatus):
        pass

    @abstractmethod
    async def delete_all_reviews_by_product_id(self, product_id: str) -> None:
        pass