from dependency_injector import containers, providers
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from src.config import settings
from src.models.product import Product


class DatabaseContainer(containers.DeclarativeContainer):
    db_client = providers.Singleton(
        AsyncIOMotorClient,
        settings.mongo.url
    )

    beanie_init = providers.Coroutine(
        init_beanie,
        database=db_client.provided[settings.mongo.db_name],
        document_models=[Product]
    )
