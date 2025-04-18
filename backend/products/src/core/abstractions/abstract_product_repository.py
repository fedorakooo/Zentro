from abc import abstractmethod, ABC

from src.core.enums.product import ProductStatus
from src.models.product import Product


class AbstractProductMongoRepository(ABC):
    @abstractmethod
    async def get_by_id(self, product_id: str) -> Product | None:
        pass

    @abstractmethod
    async def get_by_ids(self, product_ids: list[str]) -> list[Product]:
        pass

    @abstractmethod
    async def create(self, product: Product) -> Product:
        pass

    @abstractmethod
    async def update(self, product_id: str, update_data: dict) -> Product | None:
        pass

    @abstractmethod
    async def delete(self, product_id: str) -> bool:
        pass

    @abstractmethod
    async def get_products(
            self,
            name: str | None = None,
            brand: str | None = None,
            brand_id: int | None = None,
            category_id: int | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            skip: int = 0,
            limit: int = 100
    ) -> list[Product]:
        pass

    @abstractmethod
    async def change_status(self, product_id: str, new_status: ProductStatus) -> Product | None:
        pass
