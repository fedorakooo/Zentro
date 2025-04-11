from fastapi import APIRouter

from src.api.v1.endpoints import reviews

router = APIRouter(prefix="/api/v1")

router.include_router(reviews.router)
