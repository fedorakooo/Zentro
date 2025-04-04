from fastapi import FastAPI
from src.containers import Container
from src.api.v1.routers import router

app = FastAPI()

container = Container()
container.wire(modules=["src.api.v1.endpoints.products"])

app.include_router(router)


@app.on_event("startup")
async def startup():
    await container.beanie_init()
