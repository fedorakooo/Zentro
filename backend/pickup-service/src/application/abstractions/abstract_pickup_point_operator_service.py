from abc import ABC, abstractmethod

from src.models.pickup_point_operator import (
    PickupPointOperatorResponse, PickupPointOperatorCreateRequest
)


class AbstractPickupPointOperatorService(ABC):
    @abstractmethod
    def get_pickup_point_operator_by_id(
            self,
            pickup_point_operator_id: int
    ) -> PickupPointOperatorResponse:
        pass

    @abstractmethod
    def get_pickup_point_operators_by_point_id(
            self,
            pickup_point_id: int
    ) -> list[PickupPointOperatorResponse]:
        pass

    @abstractmethod
    def create_pickup_point_operator(
            self,
            pickup_create: PickupPointOperatorCreateRequest
    ) -> PickupPointOperatorResponse:
        pass

    @abstractmethod
    def delete_pickup_point_operator(
            self,
            pickup_point_operator_id: int
    ) -> None:
        pass
