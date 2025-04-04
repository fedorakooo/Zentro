from beanie import PydanticObjectId
from typing import Optional, List

from src.models.product import Product
from src.repositories.product_mongo_repository import AbstractProductMongoRepository
from src.schemas.products import ProductRead, ProductCreate, ProductUpdate
from src.services.abstract_product_service import AbstractProductService


class ProductService(AbstractProductService):
    def __init__(self, product_repository: AbstractProductMongoRepository):
        self.repository = product_repository

    async def get_product(self, product_id: PydanticObjectId) -> Optional[ProductRead]:
        product = await self.repository.get_by_id(product_id)
        if product is None:
            return None
        return ProductRead.from_orm(product)

    async def get_products(self, product_ids: List[PydanticObjectId]) -> List[ProductRead]:
        products = await self.repository.get_by_ids(product_ids)
        return [ProductRead.from_orm(product) for product in products]

    async def create_product(self, product_data: ProductCreate) -> ProductRead:
        product = Product(**product_data.dict())
        created_product = await self.repository.create(product)
        return ProductRead.from_orm(created_product)

    async def update_product(
            self,
            product_id: PydanticObjectId,
            product_update: ProductUpdate,
            partial: bool = True
    ) -> Optional[ProductRead]:
        update_data = product_update.dict()

        if not partial:
            existing = await self.get_product(product_id)
            if not existing:
                return None
            update_data = {**existing.dict(), **product_update.dict()}

        updated_product = await self.repository.update(product_id, update_data)
        if updated_product is None:
            return None
        return ProductRead.from_orm(updated_product)

    async def delete_product(self, product_id: PydanticObjectId) -> bool:
        return await self.repository.delete(product_id)

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
        products = await self.repository.search(
            name=name,
            brand=brand,
            brand_id=brand_id,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=limit
        )
        return [ProductRead.from_orm(product) for product in products]

    async def count_products(
            self,
            name: Optional[str] = None,
            brand: Optional[str] = None,
            brand_id: Optional[int] = None,
            category_id: Optional[int] = None,
            min_price: Optional[float] = None,
            max_price: Optional[float] = None
    ) -> int:
        return await self.repository.count(
            name=name,
            brand=brand,
            brand_id=brand_id,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price
        )
