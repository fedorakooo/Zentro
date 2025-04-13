import asyncio

from fastapi import FastAPI
from dependency_injector.wiring import inject

from src.models.base import Base
from src.containers.container import Container
from src.api.v1.routes import router

app = FastAPI()

container = Container()
container.wire(modules=["src.api.v1.endpoints.reviews"])

app.include_router(router)


@app.on_event("startup")
@inject
async def startup():
    engine = container.db.engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    consumer = container.consumer()
    await consumer.start()
    asyncio.create_task(consumer.consume_events())


@app.on_event("shutdown")
async def shutdown_event():
    await container.messaging.product_consumer().stop()
