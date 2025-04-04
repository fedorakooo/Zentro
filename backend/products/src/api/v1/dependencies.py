from dependency_injector.wiring import inject, Provide
from src.containers import Container

from src.repositories.product_mongo_repository import ProductMongoRepository
from src.services.product_service import ProductService


@inject
async def get_db_client(
        client=Provide[Container.db_client],
        init: callable = Provide[Container.beanie_init]
):
    await init
    return client


@inject
def get_product_repository(
        repo: ProductMongoRepository = Provide[Container.product_repository]
) -> ProductMongoRepository:
    return repo


@inject
def get_product_service(
        service: ProductService = Provide[Container.product_service]
) -> ProductService:
    return service
