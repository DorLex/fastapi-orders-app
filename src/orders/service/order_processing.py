from time import sleep

from src.database import SessionLocal
from src.orders.enums import OrderStatusEnum
from src.orders.service.crud import update_order_status, get_order_by_id


def order_processing(order_id: int):
    print(f'<Начало обработки заказа №{order_id}>')
    sleep(3)

    with SessionLocal() as db:
        db_order = get_order_by_id(db, order_id)

        if not db_order:
            raise Exception(f'Заказ №{order_id} не найден')

        update_order_status(db, db_order, OrderStatusEnum.completed)
