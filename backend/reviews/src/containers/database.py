from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dependency_injector import containers, providers


class DatabaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    engine = providers.Singleton(
        create_async_engine,
        url=config.db.url,
        echo=config.db.echo,
        pool_size=config.db.pool_size
    )

    session_factory = providers.Factory(
        async_sessionmaker,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    db_session = providers.Resource(
        session_factory
    )
