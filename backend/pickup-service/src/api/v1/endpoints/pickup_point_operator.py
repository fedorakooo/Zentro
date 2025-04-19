from fastapi import APIRouter, HTTPException, status, Depends
from dependency_injector.wiring import Provide, inject

from src.application.abstractions.abstract_pickup_point_operator_service import AbstractPickupPointOperatorService
from src.container import Container
from src.models.pickup_point_operator import (
    PickupPointOperatorResponse, PickupPointOperatorCreateRequest
)

router = APIRouter(prefix="/pickup-point-operators", tags=["Pickup Point Operators"])


@router.get("/{pickup_point_operator_id}", response_model=PickupPointOperatorResponse)
@inject
async def get_pickup_point_operator(
        pickup_point_operator_id: int,
        pickup_point_operator_service: AbstractPickupPointOperatorService = Depends(
            Provide[Container.pickup_operator_point_service]
        )
) -> PickupPointOperatorResponse:
    operator = pickup_point_operator_service.get_pickup_point_operator_by_id(pickup_point_operator_id)
    if not operator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pickup point operator not found"
        )
    return operator


@router.get("/pickup-points/{pickup_point_id}", response_model=list[PickupPointOperatorResponse])
@inject
async def get_pickup_point_operators_by_pickup_point_id(
        pickup_point_id: int,
        pickup_point_operator_service: AbstractPickupPointOperatorService = Depends(
            Provide[Container.pickup_operator_point_service]
        )
) -> list[PickupPointOperatorResponse]:
    operators = pickup_point_operator_service.get_pickup_point_operators_by_point_id(pickup_point_id)
    return operators


@router.post("/", response_model=PickupPointOperatorResponse, status_code=status.HTTP_201_CREATED)
@inject
async def create_pickup_point_operator(
        pickup_create: PickupPointOperatorCreateRequest,
        pickup_point_operator_service: AbstractPickupPointOperatorService = Depends(
            Provide[Container.pickup_operator_point_service]
        )
) -> PickupPointOperatorResponse:
    return pickup_point_operator_service.create_pickup_point_operator(pickup_create)


@router.delete("/{pickup_point_operator_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_pickup_point_operator(
        pickup_point_operator_id: int,
        pickup_point_operator_service: AbstractPickupPointOperatorService = Depends(
            Provide[Container.pickup_operator_point_service]
        )
) -> None:
    pickup_point_operator_service.delete_pickup_point_operator(pickup_point_operator_id)
