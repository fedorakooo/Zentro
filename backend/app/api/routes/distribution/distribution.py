from typing import List
from fastapi import APIRouter

from app.services.distribution.distribution import get_distribution_center_by_id, get_all_distribution_centers
from app.core.schemas.distribution import DistributionCenter

router = APIRouter(tags=["Distributions"], prefix="/distributions")


@router.get("/", response_model=List[DistributionCenter])
async def get_distribution_centers():
    distributions_centers: List[DistributionCenter] = await get_all_distribution_centers()

    return distributions_centers


@router.get("/{distribution_center_id:int}", response_model=DistributionCenter)
async def get_distribution_center(distribution_center_id: int):
    distribution_center = await get_distribution_center_by_id(distribution_center_id)

    return distribution_center
