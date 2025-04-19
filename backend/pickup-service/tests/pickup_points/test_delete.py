import pytest

from fastapi import status

from tests.pickup_points.conftest import BaseTestPickupPoint


@pytest.mark.asyncio
class TestDeletePickupPoint(BaseTestPickupPoint):
    async def test_delete_pickup_point_success(self, override_container, mock_pickup_point_service):
        mock_pickup_point_service.delete_pickup_point_by_id.return_value = None

        response = await self.make_request("delete", "/api/v1/pickup-points/1")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_pickup_point_service.delete_pickup_point_by_id.assert_called_once_with(1)

    async def test_delete_pickup_point_invalid_id(self, override_container):
        response = await self.make_request("delete", "/api/v1/pickup-points/invalid")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    async def test_delete_pickup_points_by_owner_success(self, override_container, mock_pickup_point_service):
        mock_pickup_point_service.delete_pickup_points_by_owner_id.return_value = None

        response = await self.make_request("delete", "/api/v1/pickup-points/owner/1")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_pickup_point_service.delete_pickup_points_by_owner_id.assert_called_once_with(1)

    async def test_delete_pickup_points_by_owner_invalid_id(self, override_container):
        response = await self.make_request("delete", "/api/v1/pickup-points/owner/invalid")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
