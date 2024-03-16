from time import sleep

from src.database import SessionLocal
from src.orders.enums import OrderStatusEnum
from src.orders.service.crud import get_order_by_id, update_order_status


def do_something_with_order(db_order):
    sleep(5)
    return True


def execute_order(order_id):
    with SessionLocal() as db:
        db_order = get_order_by_id(db, order_id)
        if not db_order:
            raise Exception(f'Заказ №{order_id} не найден!')

        order_processing_successful = do_something_with_order(db_order)

        if not order_processing_successful:
            raise Exception(f'Произошла ошибка при обработке Заказа №{order_id}')

        update_order_status(db, db_order, OrderStatusEnum.completed)
