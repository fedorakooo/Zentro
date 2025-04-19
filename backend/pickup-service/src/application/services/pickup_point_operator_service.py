from datetime import datetime

from src.application.abstractions.abstract_pickup_point_operator_service import AbstractPickupPointOperatorService
from src.models.pickup_point_operator import PickupPointOperatorResponse, PickupPointOperatorCreateRequest

pickup_point_operator_db: list[PickupPointOperatorResponse] = []


class PickupPointOperatorService(AbstractPickupPointOperatorService):
    def get_pickup_point_operator_by_id(
            self,
            pickup_point_operator_id: int
    ) -> PickupPointOperatorResponse:
        result = list(filter(lambda op: op.id == pickup_point_operator_id, pickup_point_operator_db))
        return result[0] if result else None

    def get_pickup_point_operators_by_point_id(
            self,
            pickup_point_id: int
    ) -> list[PickupPointOperatorResponse]:
        result = list(filter(lambda op: op.pickup_point_id == pickup_point_id, pickup_point_operator_db))
        return result

    def create_pickup_point_operator(
            self,
            pickup_create: PickupPointOperatorCreateRequest
    ) -> PickupPointOperatorResponse:
        pickup_point_operator_response = PickupPointOperatorResponse(
            id=len(pickup_point_operator_db) + 1,
            **pickup_create.dict(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        pickup_point_operator_db.append(pickup_point_operator_response)
        return pickup_point_operator_response

    def delete_pickup_point_operator(
            self,
            pickup_point_operator_id: int
    ) -> None:
        global pickup_point_operator_db
        pickup_point_operator_db = list(filter(
            lambda op: op.id != pickup_point_operator_id, 
            pickup_point_operator_db
        ))
