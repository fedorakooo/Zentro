from dependency_injector import containers, providers

from src.containers.database import DatabaseContainer
from src.infrastructure.kafka.consumers.product_consumer import ProductConsumer
from src.infrastructure.kafka.producers.product_producer import ProductProducer
from src.infrastructure.repositories.mongo.product_repository import ProductMongoRepository
from src.application.services.product_service import ProductService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["src.api.v1.endpoints.products"]
    )

    database = providers.Container(DatabaseContainer)

    product_repository = providers.Factory(
        ProductMongoRepository
    )

    product_producer = providers.Factory(
        ProductProducer
    )

    product_service = providers.Factory(
        ProductService,
        product_repository=product_repository,
        product_producer=product_producer
    )

    product_consumer = providers.Factory(
        ProductConsumer,
        product_service=product_service
    )