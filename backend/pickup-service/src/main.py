from fastapi import FastAPI

from src.api.v1.router import router
from src.container import Container

app = FastAPI()

container = Container()

app.include_router(router)
