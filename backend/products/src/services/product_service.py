from src.models.product import Product
from src.repositories.mongo.product_repository import AbstractProductMongoRepository
from src.schemas.products import ProductRead, ProductCreate, ProductUpdate
from src.services.abstract_product_service import AbstractProductService


class ProductService(AbstractProductService):
    def __init__(self, product_repository: AbstractProductMongoRepository):
        self.repository = product_repository

    async def get_product(self, product_id: str) -> ProductRead | None:
        product = await self.repository.get_by_id(product_id)
        if product is None:
            return None
        return ProductRead.from_orm(product)

    async def get_products(self, product_ids: list[str]) -> list[ProductRead]:
        products = await self.repository.get_by_ids(product_ids)
        return [ProductRead.from_orm(product) for product in products]

    async def create_product(self, product_data: ProductCreate) -> ProductRead:
        product = Product(**product_data.dict())
        created_product = await self.repository.create(product)
        return ProductRead.from_orm(created_product)

    async def update_product(
            self,
            product_id: str,
            product_update: ProductUpdate,
            partial: bool = True
    ) -> list[ProductRead]:
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

    async def delete_product(self, product_id: str) -> bool:
        return await self.repository.delete(product_id)

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
            name: str | None = None,
            brand: str | None = None,
            brand_id: int | None = None,
            category_id: int | None = None,
            min_price: float | None = None,
            max_price: float | None = None
    ) -> int:
        return await self.repository.count(
            name=name,
            brand=brand,
            brand_id=brand_id,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price
        )
