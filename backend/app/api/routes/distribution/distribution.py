from fastapi import APIRouter

from app.core.schemas.distribution import DistributionCenter
from app.services.distribution.distribution import get_distribution_center_by_id

router = APIRouter(tags=["Distributions"], prefix="/distributions")

@router.get("/{distribution_center_id:int}", response_model=DistributionCenter)
async def get_distribution_center(distribution_center_id: int):
    distribution_center = await get_distribution_center_by_id(distribution_center_id)

    return distribution_center