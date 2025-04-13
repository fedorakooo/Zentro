from abc import ABC, abstractmethod

from src.enums.review_status import ReviewStatus
from src.models.review import ReviewORM


class AbstractReviewRepository(ABC):
    @abstractmethod
    async def get_review_by_id(self, review_id: int) -> ReviewORM:
        pass

    @abstractmethod
    async def get_product_reviews(
            self,
            product_id: str,
            rating: int | None,
            skip: int = 0,
            limit: int = 100
    ) -> list[ReviewORM]:
        pass

    @abstractmethod
    async def create_review(self, review: ReviewORM) -> ReviewORM:
        pass

    @abstractmethod
    async def change_review_status(self, review_id: int, original_status: ReviewStatus):
        pass

    @abstractmethod
    async def delete_review_by_id(self, review_id: int) -> None:
        pass

    @abstractmethod
    async def delete_reviews_by_product_id(self, product_id: str) -> None:
        pass