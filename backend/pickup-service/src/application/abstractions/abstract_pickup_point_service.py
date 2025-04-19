from abc import ABC

from src.models.pickup_point import PickupPointResponse, PickupPointCreateRequest


class AbstractPickupPointService(ABC):
    def get_pickup_point_by_id(self, pickup_point_id: int) -> PickupPointResponse:
        pass

    def get_pickup_points_by_owner_id(self, pickup_owner_id: int) -> list[PickupPointResponse]:
        pass

    def get_all_pickup_points(self) -> list[PickupPointResponse]:
        pass

    def create_pickup_point(self, pickup_create: PickupPointCreateRequest) -> PickupPointResponse:
        pass

    def delete_pickup_points_by_owner_id(self, pickup_owner_id: int) -> None:
        pass

    def delete_pickup_point_by_id(self, pickup_point_id: int) -> None:
        pass

