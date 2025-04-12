from abc import ABC, abstractmethod

from src.models.review import ReviewORM


class AbstractReviewRepository(ABC):
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
    async def create(self, review: ReviewORM) -> ReviewORM:
        pass
