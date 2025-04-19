from dependency_injector import containers, providers

from src.application.services.pickup_point_operator_service import PickupPointOperatorService
from src.application.services.pickup_point_service import PickupPointService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.api.v1.endpoints.pickup_point",
            "src.api.v1.endpoints.pickup_point_operator",
        ]
    )

    pickup_operator_point_service = providers.Factory(
        PickupPointOperatorService
    )

    pickup_point_service = providers.Factory(
        PickupPointService
    )
