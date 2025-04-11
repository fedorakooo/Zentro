from abc import ABC, abstractmethod

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
    async def create(self, review: ReviewCreate) -> ReviewRead:
        pass
