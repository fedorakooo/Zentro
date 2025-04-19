import pytest

from fastapi import status

from tests.pickup_point_operator.conftest import BaseTestPickupPointOperator


@pytest.mark.asyncio
class TestDeletePickupPointOperator(BaseTestPickupPointOperator):
    async def test_delete_operator_success(self, override_container, mock_pickup_point_operator_service):
        mock_pickup_point_operator_service.delete_pickup_point_operator.return_value = None

        response = await self.make_request("delete", "/api/v1/pickup-point-operators/1")

        assert response.status_code == status.HTTP_204_NO_CONTENT
        mock_pickup_point_operator_service.delete_pickup_point_operator.assert_called_once_with(1)

    async def test_delete_operator_invalid_id(self, override_container):
        response = await self.make_request("delete", "/api/v1/pickup-point-operators/invalid")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
