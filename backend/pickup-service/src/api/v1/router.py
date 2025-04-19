from fastapi import APIRouter

from src.api.v1.endpoints.pickup_point_operator import router as pickup_operator_router
from src.api.v1.endpoints.pickup_point import router as pickup_point_router

router = APIRouter(prefix="/api/v1")

router.include_router(pickup_operator_router)
router.include_router(pickup_point_router)
