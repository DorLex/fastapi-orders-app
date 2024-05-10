import pytest

from src.orders.models import OrderModel
from src.orders.repository import OrderRepository
from src.orders.schemas import OrderCreateSchema
from tests.conftest import SessionTest


@pytest.fixture(scope='session')
async def base_test_order_data():
    return {
        'title': 'base_test_order',
        'description': 'base_test_order description'
    }


@pytest.fixture(scope='session', autouse=True)
async def base_test_order(prepare_db, base_test_user, base_test_order_data):
    order = OrderCreateSchema(**base_test_order_data)

    async with SessionTest() as db:
        db_order: OrderModel = await OrderRepository(db).create(base_test_user, order)
        return db_order
