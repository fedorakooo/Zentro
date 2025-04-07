from abc import abstractmethod, ABC

from src.schemas.products import ProductRead, ProductCreate, ProductUpdate


class AbstractProductService(ABC):
    @abstractmethod
    async def get_product(self, product_id: str) -> ProductRead | None:
        pass

    @abstractmethod
    async def get_products(self, product_ids: list[str]) -> list[ProductRead]:
        pass

    @abstractmethod
    async def create_product(self, product_data: ProductCreate) -> ProductRead:
        pass

    @abstractmethod
    async def update_product(
            self,
            product_id: str,
            product_update: ProductUpdate,
            partial: bool = True
    ) -> ProductRead | None:
        pass

    @abstractmethod
    async def delete_product(self, product_id: str) -> bool:
        pass

    @abstractmethod
    async def search_products(
            self,
            name: str | None = None,
            brand: str | None = None,
            brand_id: int | None = None,
            category_id: int | None = None,
            min_price: float | None = None,
            max_price: float | None = None,
            skip: int = 0,
            limit: int = 100
    ) -> list[ProductRead]:
        pass

    @abstractmethod
    async def count_products(
            self,
            name: str | None = None,
            brand: str | None = None,
            brand_id: int | None = None,
            category_id: int | None = None,
            min_price: float | None = None,
            max_price: float | None = None
    ) -> int:
        pass
