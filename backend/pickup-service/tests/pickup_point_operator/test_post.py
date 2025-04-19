import pytest

from fastapi import status

from tests.pickup_point_operator.conftest import BaseTestPickupPointOperator


@pytest.mark.asyncio
class TestCreatePickupPointOperator(BaseTestPickupPointOperator):
    async def test_create_operator_success(
            self,
            override_container,
            mock_pickup_point_operator_service,
            sample_operator,
            create_operator_data
    ):
        mock_pickup_point_operator_service.create_pickup_point_operator.return_value = sample_operator

        response = await self.make_request("post", "/api/v1/pickup-point-operators/", json=create_operator_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["name"] == create_operator_data["name"]
        assert response_data["email"] == create_operator_data["email"]
        mock_pickup_point_operator_service.create_pickup_point_operator.assert_called_once()

    async def test_create_operator_invalid_data(self, override_container):
        invalid_data = {
            "pickup_point_id": "invalid",
            "name": "John Doe",
            "email": "not-an-email",
            "phone_number": "123",
            "password": "short"
        }

        response = await self.make_request("post", "/api/v1/pickup-point-operators/", json=invalid_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
