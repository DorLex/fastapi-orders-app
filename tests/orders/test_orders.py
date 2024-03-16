import pytest

from src.orders.service.crud import update_order_status
from tests.conftest import SessionTest


class TestOrders:
    def test_update_order_status(self, base_test_order):
        with SessionTest() as db:
            with pytest.raises(ValueError):
                update_order_status(db, base_test_order, 'incorrect_status')
