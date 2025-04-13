from src.core.enums.product import ProductStatus
from src.core.exceptions.product_exceptions import HttpProductNotFoundError
from src.infrastructure.elasticsearch.products.service import ElasticProductService
from src.infrastructure.kafka.producers.product_producer import ProductProducer
from src.models.product import Product
from src.infrastructure.mongo.product_repository import AbstractProductMongoRepository
from src.schemas.products import ProductRead, ProductCreate, ProductUpdate
from src.application.abstractions.abstract_product_service import AbstractProductService
from src.schemas.saga import SagaResponse


class ProductService(AbstractProductService):
    def __init__(
            self,
            product_repository: AbstractProductMongoRepository,
            product_producer: ProductProducer,
            elastic_product_service: ElasticProductService
    ):
        self.repository = product_repository
        self.product_producer = product_producer
        self.elastic_product_service = elastic_product_service

    async def get_product(self, product_id: str) -> ProductRead | None:
        product = await self.repository.get_by_id(product_id)
        if product is None:
            return None
        return ProductRead.from_orm(product)

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
    ) -> list[ProductRead]:
        product_ids = await self.elastic_product_service.get_products(
            name=name,
            brand=brand,
            brand_id=brand_id,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            skip=skip,
            limit=limit
        )
        products = await self.repository.get_by_ids(product_ids)
        return [ProductRead.from_orm(product) for product in products]

    async def create_product(self, product_data: ProductCreate) -> ProductRead:
        product = Product(**product_data.dict(), status=ProductStatus.DRAFT)
        created_product = await self.repository.create(product)
        await self.elastic_product_service.create_product(
            product_id=created_product.id,
            product=product_data.dict()
        )
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
        await self.elastic_product_service.update_product(
            product_id=product_id,
            product=product_update.dict()
        )
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
        await self.elastic_product_service.delete_product(product_id)

        return SagaResponse(
            success=True,
            message="Product deletion started",
            compensation_data={
                "product_id": product_id,
                "original_status": product.status
            }
        )

    async def compensate_delete_product(self, product_id: str, original_status: ProductStatus) -> None:
        await self.product_producer.start()

        await self.product_producer.send_compensation_event(
            product_id=product_id
        )

        await self.product_producer.stop()

        await self.repository.change_status(product_id, original_status)

        return SagaResponse(
            success=True,
            message="Product compensate started",
            compensation_data={
                "product_id": product_id
            }
        )
