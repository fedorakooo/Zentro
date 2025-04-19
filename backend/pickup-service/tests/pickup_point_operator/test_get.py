import pytest

from fastapi import status

from tests.pickup_point_operator.conftest import BaseTestPickupPointOperator


@pytest.mark.asyncio
class TestGetPickupPointOperator(BaseTestPickupPointOperator):
    async def test_get_operator_success(self, override_container, mock_pickup_point_operator_service, sample_operator):
        mock_pickup_point_operator_service.get_pickup_point_operator_by_id.return_value = sample_operator

        response = await self.make_request("get", "/api/v1/pickup-point-operators/1")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == sample_operator.id
        assert response_data["name"] == sample_operator.name
        mock_pickup_point_operator_service.get_pickup_point_operator_by_id.assert_called_once_with(1)

    async def test_get_operator_not_found(self, override_container, mock_pickup_point_operator_service):
        mock_pickup_point_operator_service.get_pickup_point_operator_by_id.return_value = None

        response = await self.make_request("get", "/api/v1/pickup-point-operators/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Pickup point operator not found"}
        mock_pickup_point_operator_service.get_pickup_point_operator_by_id.assert_called_once_with(999)

    async def test_get_operator_invalid_id(self, override_container):
        response = await self.make_request("get", "/api/v1/pickup-point-operators/invalid")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestGetPickupPointOperatorsByPointId(BaseTestPickupPointOperator):
    async def test_get_operators_by_point_success(self, override_container, mock_pickup_point_operator_service,
                                                  sample_operator):
        mock_pickup_point_operator_service.get_pickup_point_operators_by_point_id.return_value = [sample_operator]

        response = await self.make_request("get", "/api/v1/pickup-point-operators/pickup-points/1")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert response_data[0]["pickup_point_id"] == sample_operator.pickup_point_id
        mock_pickup_point_operator_service.get_pickup_point_operators_by_point_id.assert_called_once_with(1)

    async def test_get_operators_by_point_empty(self, override_container, mock_pickup_point_operator_service):
        mock_pickup_point_operator_service.get_pickup_point_operators_by_point_id.return_value = []

        response = await self.make_request("get", "/api/v1/pickup-point-operators/pickup-points/999")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
        mock_pickup_point_operator_service.get_pickup_point_operators_by_point_id.assert_called_once_with(999)
