import pytest

from fastapi import status

from tests.pickup_points.conftest import BaseTestPickupPoint


@pytest.mark.asyncio
class TestCreatePickupPoint(BaseTestPickupPoint):
    async def test_create_pickup_point_success(
            self,
            override_container,
            mock_pickup_point_service,
            sample_pickup_point
    ):
        create_data = {
            "address": sample_pickup_point.address,
            "latitude": sample_pickup_point.latitude,
            "longitude": sample_pickup_point.longitude,
            "working_hours": sample_pickup_point.working_hours,
            "phone": sample_pickup_point.phone,
            "email": sample_pickup_point.email,
            "description": sample_pickup_point.description
        }
        mock_pickup_point_service.create_pickup_point.return_value = sample_pickup_point

        response = await self.make_request("post", "/api/v1/pickup-points/", json=create_data)

        assert response.status_code == status.HTTP_201_CREATED
        response_data = response.json()
        assert response_data["address"] == create_data["address"]
        assert response_data["working_hours"] == create_data["working_hours"]
        mock_pickup_point_service.create_pickup_point.assert_called_once()
