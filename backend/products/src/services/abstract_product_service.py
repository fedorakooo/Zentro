from abc import abstractmethod, ABC

from beanie import PydanticObjectId
from typing import Optional, List

from src.schemas.products import ProductRead, ProductCreate, ProductUpdate


class AbstractProductService(ABC):
    @abstractmethod
    async def get_product(self, product_id: PydanticObjectId) -> Optional[ProductRead]:
        pass

    @abstractmethod
    async def get_products(self, product_ids: List[PydanticObjectId]) -> List[ProductRead]:
        pass

    @abstractmethod
    async def create_product(self, product_data: ProductCreate) -> ProductRead:
        pass

    @abstractmethod
    async def update_product(
            self,
            product_id: PydanticObjectId,
            product_update: ProductUpdate,
            partial: bool = True
    ) -> Optional[ProductRead]:
        pass

    @abstractmethod
    async def delete_product(self, product_id: PydanticObjectId) -> bool:
        pass

    @abstractmethod
    async def search_products(
            self,
            name: Optional[str] = None,
            brand: Optional[str] = None,
            brand_id: Optional[int] = None,
            category_id: Optional[int] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None,
            skip: int = 0,
            limit: int = 100
    ) -> List[ProductRead]:
        pass

    @abstractmethod
    async def count_products(
            self,
            name: Optional[str] = None,
            brand: Optional[str] = None,
            brand_id: Optional[int] = None,
            category_id: Optional[int] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> int:
        pass
