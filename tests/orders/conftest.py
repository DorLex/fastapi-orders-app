import pytest

from src.orders.schemas import OrderInSchema
from src.orders.service_old.crud import create_order
from tests.conftest import SessionTest


@pytest.fixture(scope='session')
def base_test_order_data():
    return {
        'title': 'base_test_order',
        'description': 'base_test_order description'
    }


@pytest.fixture(scope='session', autouse=True)
def base_test_order(prepare_db, base_test_user, base_test_order_data):
    order = OrderInSchema(**base_test_order_data)

    with SessionTest() as db:
        db_order = create_order(db, base_test_user, order)
        return db_order
