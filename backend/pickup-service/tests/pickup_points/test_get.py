import pytest

from fastapi import status

from tests.pickup_points.conftest import BaseTestPickupPoint


@pytest.mark.asyncio
class TestGetPickupPointById(BaseTestPickupPoint):
    async def test_get_pickup_point_success(self, override_container, mock_pickup_point_service, sample_pickup_point):
        mock_pickup_point_service.get_pickup_point_by_id.return_value = sample_pickup_point

        response = await self.make_request("get", "/api/v1/pickup-points/1")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert response_data["id"] == sample_pickup_point.id
        assert response_data["address"] == sample_pickup_point.address
        assert response_data["status"] == sample_pickup_point.status.value
        mock_pickup_point_service.get_pickup_point_by_id.assert_called_once_with(1)

    async def test_get_pickup_point_not_found(self, override_container, mock_pickup_point_service):
        mock_pickup_point_service.get_pickup_point_by_id.return_value = None

        response = await self.make_request("get", "/api/v1/pickup-points/999")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"detail": "Pickup point not found"}
        mock_pickup_point_service.get_pickup_point_by_id.assert_called_once_with(999)

    async def test_get_pickup_point_invalid_id(self, override_container):
        response = await self.make_request("get", "/api/v1/pickup-points/invalid")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
class TestGetPickupPointsByOwner(BaseTestPickupPoint):
    async def test_get_by_owner_success(self, override_container, mock_pickup_point_service, sample_pickup_point):
        mock_pickup_point_service.get_pickup_points_by_owner_id.return_value = [sample_pickup_point]

        response = await self.make_request("get", "/api/v1/pickup-points/owner/1")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert response_data[0]["owner_id"] == sample_pickup_point.owner_id
        mock_pickup_point_service.get_pickup_points_by_owner_id.assert_called_once_with(1)

    async def test_get_by_owner_empty(self, override_container, mock_pickup_point_service):
        mock_pickup_point_service.get_pickup_points_by_owner_id.return_value = []

        response = await self.make_request("get", "/api/v1/pickup-points/owner/999")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []
        mock_pickup_point_service.get_pickup_points_by_owner_id.assert_called_once_with(999)


@pytest.mark.asyncio
class TestGetPickupPointsMapData(BaseTestPickupPoint):
    async def test_get_map_data_success(self, override_container, mock_pickup_point_service, sample_pickup_point):
        mock_pickup_point_service.get_all_pickup_points.return_value = [sample_pickup_point]

        response = await self.make_request("get", "/api/v1/pickup-points/map-data/")

        assert response.status_code == status.HTTP_200_OK
        response_data = response.json()
        assert isinstance(response_data, list)
        assert response_data[0]["id"] == sample_pickup_point.id
        mock_pickup_point_service.get_all_pickup_points.assert_called_once()
