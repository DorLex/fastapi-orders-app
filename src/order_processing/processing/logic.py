from time import sleep

from src.database import SessionLocal
from src.orders.enums import OrderStatusEnum
from src.orders.service_old.crud import get_order_by_id, update_order_status


def do_something_with_order(db_order):
    sleep(5)
    return True


def execute_order(order_id):
    with SessionLocal() as db:
        db_order = get_order_by_id(db, order_id)
        if not db_order:
            raise Exception(f'Заказ №{order_id} не найден!')

        if db_order.status == OrderStatusEnum.created:
            update_order_status(db, db_order, OrderStatusEnum.in_processing)

            order_processing_successful = do_something_with_order(db_order)

            if not order_processing_successful:
                update_order_status(db, db_order, OrderStatusEnum.failed)
                raise Exception(f'Произошла ошибка при обработке Заказа №{order_id}')

            update_order_status(db, db_order, OrderStatusEnum.completed)
