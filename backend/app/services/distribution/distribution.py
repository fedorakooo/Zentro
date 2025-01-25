from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from app.core.models.distribution import DistributionCenterORM
from app.core.schemas.distribution import DistributionCenter
from app.dependencies.db import get_db


async def get_distribution_center_by_id(distribution_center_id: int) -> DistributionCenter:
    async with get_db() as db:
        try:
            query = select(DistributionCenterORM).where(DistributionCenterORM.id == distribution_center_id)
            result = await db.execute(query)

            distribution_center_db = result.scalars().one_or_none()

            if not distribution_center_db:
                raise HTTPException(
                    status_code=404,
                    detail="Distribution not found"
                )

            distribution_center = DistributionCenter.from_orm(distribution_center_db)

            return distribution_center

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail="An unexpected error occurred while fetching the product",
            )
