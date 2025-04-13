from dependency_injector import containers, providers

from src.application.services.review_service import ReviewService
from src.config import settings
from src.containers.database import DatabaseContainer
from src.infrastructure.kafka.consumers.consumer import Consumer
from src.infrastructure.kafka.producers.producer import Producer
from src.infrastructure.repositories.implementations.postgre_review_repository import ReviewPostgreRepository


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.api.v1.endpoints.reviews"])

    db = providers.Container(DatabaseContainer)

    db.config.from_dict({
        "db": {
            "url": settings.db.url,
            "echo": settings.db.echo,
            "pool_size": settings.db.pool_size
        }
    })

    review_repository = providers.Factory(
        ReviewPostgreRepository,
        session_factory=db.session_factory
    )

    producer = providers.Factory(
        Producer
    )

    review_service = providers.Factory(
        ReviewService,
        review_repository=review_repository,
        producer=producer
    )

    consumer = providers.Factory(
        Consumer,
        review_service=review_service
    )
