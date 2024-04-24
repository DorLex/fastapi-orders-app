import pytest
from aiokafka import AIOKafkaProducer
from starlette import status

from src.orders.enums import OrderStatusEnum
from src.orders.models import OrderModel
from src.orders.repository import OrderRepository
from tests.conftest import SessionTest


class TestOrdersPositive:
    order_data = {
        'title': 'test_order_1',
        'description': 'test_order_1 description'
    }

    async def mock_send_and_wait(*args, **kwargs):
        return True

    def test_read_orders(self, client, auth_headers):
        response = client.get('/orders', headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()) > 0

    def test_add_order(self, client, auth_headers, monkeypatch):
        monkeypatch.setattr(AIOKafkaProducer, 'send_and_wait', self.mock_send_and_wait)

        response = client.post('/orders', json=self.order_data, headers=auth_headers)
        assert response.status_code == status.HTTP_201_CREATED, response.text

        order_id = response.json().get('order_id')
        with SessionTest() as db:
            db_order: OrderModel = OrderRepository(db).get_by_id(order_id)
            assert db_order.title == self.order_data.get('title')
            assert db_order.description == self.order_data.get('description')

    def test_read_my_orders(self, client, auth_headers):
        response = client.get('/orders/my/', headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()) > 0

    def test_update_order_status(self, base_test_order):
        with SessionTest() as db:
            db_order: OrderModel = OrderRepository(db).update_status(base_test_order, OrderStatusEnum.completed)
            assert db_order.status == OrderStatusEnum.completed


class TestOrdersNegative:
    incorrect_order_data = {
        'title': 'test_order_2'
    }

    def test_add_order(self, client, auth_headers):
        response = client.post('/orders', json=self.incorrect_order_data, headers=auth_headers)
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text

    def test_update_order_status(self, base_test_order):
        with SessionTest() as db:
            with pytest.raises(ValueError):
                OrderRepository(db).update_status(base_test_order, 'incorrect_status')  # type: ignore
