import datetime

from src.application.abstractions.abstract_pickup_point_service import AbstractPickupPointService
from src.core.enums.pickup_point import PickupPointStatus
from src.models.pickup_point import PickupPointResponse, PickupPointCreateRequest

pickup_point_db: list[PickupPointResponse] = []


class PickupPointService(AbstractPickupPointService):
    def get_pickup_point_by_id(self, pickup_point_id: int) -> PickupPointResponse | None:
        result = list(filter(lambda point: point.id == pickup_point_id, pickup_point_db))
        return result[0] if result else None

    def get_pickup_points_by_owner_id(self, pickup_owner_id: int) -> PickupPointResponse | None:
        return list(filter(lambda point: point.owner_id == pickup_owner_id, pickup_point_db))

    def get_all_pickup_points(self) -> list[PickupPointResponse]:
        return pickup_point_db

    def create_pickup_point(self, pickup_create: PickupPointCreateRequest) -> PickupPointResponse:
        pickup_point_response = PickupPointResponse(
            id=len(pickup_point_db) + 1,
            owner_id=0,
            **pickup_create.dict(),
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
            status=PickupPointStatus.ACTIVE
        )
        pickup_point_db.append(pickup_point_response)
        return pickup_point_response

    def delete_pickup_point_by_id(self, pickup_point_id: int) -> None:
        global pickup_point_db
        pickup_point_db = list(filter(lambda x: x.id != pickup_point_id, pickup_point_db))

    def delete_pickup_points_by_owner_id(self, pickup_owner_id: int) -> None:
        global pickup_point_db
        pickup_point_db = list(filter(lambda x: x.owner_id != pickup_owner_id, pickup_point_db))
