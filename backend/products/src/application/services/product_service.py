from src.enums.product import ProductStatus
from src.exceptions.product_exceptions import HttpProductNotFoundError
from src.infrastructure.kafka.producers.product_producer import ProductProducer
from src.models.product import Product
from src.infrastructure.repositories.mongo.product_repository import AbstractProductMongoRepository
from src.schemas.products import ProductRead, ProductCreate, ProductUpdate
from src.application.abstractions.abstract_product_service import AbstractProductService
from src.schemas.saga import SagaResponse


class ProductService(AbstractProductService):
    def __init__(
            self,
            product_repository: AbstractProductMongoRepository,
            product_producer: ProductProducer
    ):
        self.repository = product_repository
        self.product_producer = product_producer

    async def get_product(self, product_id: str) -> ProductRead | None:
        product = await self.repository.get_by_id(product_id)
        if product is None:
            return None
        return ProductRead.from_orm(product)

    async def get_products(self, product_ids: list[str]) -> list[ProductRead]:
        products = await self.repository.get_by_ids(product_ids)
        return [ProductRead.from_orm(product) for product in products]

    async def create_product(self, product_data: ProductCreate) -> ProductRead:
        product = Product(**product_data.dict(), status=ProductStatus.DRAFT)
        created_product = await self.repository.create(product)
        return ProductRead.from_orm(created_product)

    async def update_product(
            self,
            product_id: str,
            product_update: ProductUpdate
    ) -> list[ProductRead]:
        existing = await self.get_product(product_id)
        if not existing:
            return None
        update_data = {**existing.dict(), **product_update.dict()}

        updated_product = await self.repository.update(product_id, update_data)
        if updated_product is None:
            return None
        return ProductRead.from_orm(updated_product)

    async def delete_product(self, product_id: str) -> SagaResponse:
        product = await self.repository.get_by_id(product_id)
        if product is None:
            return HttpProductNotFoundError(product_id)

        await self.product_producer.start()

        await self.product_producer.send_delete_event(
            product_id=product_id,
            original_status=product.status
        )

        await self.product_producer.stop()

        await self.repository.delete(product_id)

        return SagaResponse(
            success=True,
            message="Product deletion started",
            compensation_data={
                "product_id": product_id,
                "original_status": product.status
            }
        )

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

    async def compensate_delete_product(self, product_id: str, original_status: ProductStatus) -> None:
        await self.repository.change_status(product_id, original_status)
