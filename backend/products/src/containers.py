from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.models.product import Product
from src.repositories.mongo.product_repository import ProductMongoRepository
from src.application.services.product_service import ProductService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.api.v1.endpoints.products"])

    config = providers.Configuration()

    db_client = providers.Singleton(
        AsyncIOMotorClient,
        "mongodb://localhost:27017"
    )

    beanie_init = providers.Coroutine(
        init_beanie,
        database=db_client.provided["product_db"],
        document_models=[Product]
    )

    product_repository = providers.Factory(
        ProductMongoRepository
    )

    product_service = providers.Factory(
        ProductService,
        product_repository=product_repository
    )