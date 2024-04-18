import pytest
from starlette import status

from src.orders.enums import OrderStatusEnum
from src.orders.models import OrderModel
from src.orders.repository import OrderRepository
from tests.conftest import SessionTest


class TestOrdersPositive:

    def test_read_orders(self, client, auth_headers):
        response = client.get('/orders', headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()) > 0

    def test_read_my_orders(self, client, auth_headers):
        response = client.get('/orders/my/', headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()) > 0

    def test_update_order_status(self, base_test_order):
        with SessionTest() as db:
            db_order: OrderModel = OrderRepository(db).update_status(base_test_order, OrderStatusEnum.completed)
            assert db_order.status == OrderStatusEnum.completed


class TestOrdersNegative:
    def test_update_order_status(self, base_test_order):
        with SessionTest() as db:
            with pytest.raises(ValueError):
                OrderRepository(db).update_status(base_test_order, 'incorrect_status')  # type: ignore
