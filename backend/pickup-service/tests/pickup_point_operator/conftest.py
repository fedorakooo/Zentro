import pytest

from datetime import datetime
from unittest.mock import Mock
from dependency_injector.providers import Factory
from httpx import AsyncClient, ASGITransport

from src.container import Container
from src.application.abstractions.abstract_pickup_point_operator_service import AbstractPickupPointOperatorService
from src.models.pickup_point_operator import PickupPointOperatorResponse, PickupPointOperatorCreateRequest
from src.main import app


class BaseTestPickupPointOperator:
    @pytest.fixture
    def container(self):
        return Container()

    @pytest.fixture
    def mock_pickup_point_operator_service(self):
        return Mock(spec=AbstractPickupPointOperatorService)

    @pytest.fixture
    def override_container(self, container, mock_pickup_point_operator_service):
        container.pickup_operator_point_service.override(Factory(lambda: mock_pickup_point_operator_service))
        return container

    @pytest.fixture
    def sample_operator(self):
        return PickupPointOperatorResponse(
            id=1,
            pickup_point_id=1,
            name="John Doe",
            email="operator@example.com",
            phone_number="+375291234567",
            password="hashed_password",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    @pytest.fixture
    def create_operator_data(self):
        return {
            "pickup_point_id": 1,
            "name": "John Doe",
            "email": "operator@example.com",
            "phone_number": "+375291234567",
            "password": "password123"
        }

    async def make_request(self, method: str, url: str, **kwargs):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            return await getattr(ac, method)(url, **kwargs)
