import asyncio

from fastapi import FastAPI
from dependency_injector.wiring import inject

from src.containers.container import Container
from src.api.v1.routers import router

app = FastAPI()

container = Container()

app.include_router(router)


@app.on_event("startup")
@inject
async def startup():
    await container.database.beanie_init()
    consumer = container.product_consumer()
    await consumer.start()
    asyncio.create_task(consumer.consume_events())


@app.on_event("shutdown")
async def shutdown_event():
    await container.messaging.product_consumer().stop()
