from dependency_injector import containers, providers

from src.application.services.review_service import ReviewService
from src.config import settings
from src.containers.database import DatabaseContainer
from src.repositories.postgre.review_postgre_repository import ReviewPostgreRepository


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

    review_service = providers.Factory(
        ReviewService,
        review_repository=review_repository
    )
