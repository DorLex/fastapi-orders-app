from time import sleep

from src.database import SessionLocal
from src.orders.enums import OrderStatusEnum
from src.orders.models import OrderModel
from src.orders.service import OrderService


def do_something_with_order(_):
    sleep(5)
    return True


def execute_order(order_id):
    with SessionLocal() as db:
        order_service = OrderService(db)

        db_order: OrderModel = order_service.get_by_id(order_id)

        if not db_order:
            raise Exception(f'Заказ №{order_id} не найден!')

        if db_order.status == OrderStatusEnum.created:
            order_service.update_status(db_order, OrderStatusEnum.in_processing)

            order_processing_successful = do_something_with_order(db_order)

            if not order_processing_successful:
                order_service.update_status(db_order, OrderStatusEnum.failed)
                raise Exception(f'Произошла ошибка при обработке Заказа №{order_id}')

            order_service.update_status(db_order, OrderStatusEnum.completed)
