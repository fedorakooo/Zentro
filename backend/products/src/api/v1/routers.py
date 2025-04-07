from fastapi import APIRouter

from src.api.v1.endpoints import products

router = APIRouter(prefix="/api/v1")

router.include_router(products.router)
