from fastapi import APIRouter, HTTPException, status, Depends
from dependency_injector.wiring import inject, Provide

from src.application.abstractions.abstract_pickup_point_service import AbstractPickupPointService
from src.container import Container
from src.models.pickup_point import (
    PickupPointResponse, PickupPointCreateRequest
)

router = APIRouter(prefix="/pickup-points", tags=["Pickup Points"])


@router.get("/{pickup_point_id}", response_model=PickupPointResponse)
@inject
async def get_pickup_point(
        pickup_point_id: int,
        pickup_point_service: AbstractPickupPointService = Depends(Provide[Container.pickup_point_service])
) -> PickupPointResponse:
    point = pickup_point_service.get_pickup_point_by_id(pickup_point_id)
    if not point:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pickup point not found"
        )
    return point


@router.get("/map-data/", response_model=list[PickupPointResponse])
@inject
async def get_pickup_points_for_map(
        pickup_point_service: AbstractPickupPointService = Depends(Provide[Container.pickup_point_service])
) -> list[PickupPointResponse]:
    return pickup_point_service.get_all_pickup_points()


@router.get("/owner/{owner_id}", response_model=list[PickupPointResponse])
@inject
async def get_pickup_points_by_owner(
        owner_id: int,
        pickup_point_service: AbstractPickupPointService = Depends(Provide[Container.pickup_point_service])
) -> list[PickupPointResponse]:
    points = pickup_point_service.get_pickup_points_by_owner_id(owner_id)
    return list(points)


@router.post("/", response_model=PickupPointResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_pickup_point(
        pickup_create: PickupPointCreateRequest,
        pickup_point_service: AbstractPickupPointService = Depends(Provide[Container.pickup_point_service])
) -> PickupPointResponse:
    return pickup_point_service.create_pickup_point(pickup_create)


@router.delete("/{pickup_point_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_pickup_point_by_id(
        pickup_point_id: int,
        pickup_point_service: AbstractPickupPointService = Depends(Provide[Container.pickup_point_service])
) -> None:
    pickup_point_service.delete_pickup_point_by_id(pickup_point_id)


@router.delete("/owner/{owner_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_pickup_points_by_owner(
        owner_id: int,
        pickup_point_service: AbstractPickupPointService = Depends(Provide[Container.pickup_point_service])
) -> None:
    pickup_point_service.delete_pickup_points_by_owner_id(owner_id)
