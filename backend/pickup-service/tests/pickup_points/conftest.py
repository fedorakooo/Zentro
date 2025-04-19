import pytest

from datetime import datetime
from unittest.mock import Mock
from dependency_injector.providers import Factory
from httpx import AsyncClient, ASGITransport

from src.container import Container
from src.application.abstractions.abstract_pickup_point_service import AbstractPickupPointService
from src.core.enums.pickup_point import PickupPointStatus
from src.models.pickup_point import PickupPointResponse
from src.main import app


class BaseTestPickupPoint:
    @pytest.fixture
    def container(self):
        return Container()

    @pytest.fixture
    def mock_pickup_point_service(self):
        return Mock(spec=AbstractPickupPointService)

    @pytest.fixture
    def override_container(self, container, mock_pickup_point_service):
        container.pickup_point_service.override(Factory(lambda: mock_pickup_point_service))
        return container

    @pytest.fixture
    def sample_pickup_point(self):
        return PickupPointResponse(
            id=1,
            owner_id=1,
            address="проспект Независимости, 58, Минск",
            latitude=53.9178,
            longitude=27.5869,
            working_hours="9:00-18:00",
            status=PickupPointStatus.ACTIVE,
            phone="+375291234567",
            email="pickup-minsk@example.com",
            description="Пункт выдачи товара возле ст.м. Площадь Якуба Коласа",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    async def make_request(self, method: str, url: str, **kwargs):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            return await getattr(ac, method)(url, **kwargs)
