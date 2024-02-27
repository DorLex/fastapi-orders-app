from time import sleep

from src.orders.enums import OrderStatusEnum
from src.orders.service.crud import update_order_status


def order_processing(db, order):
    print(f'Начало обработки заказа {order.title}')
    sleep(5)

    update_order_status(db, order, OrderStatusEnum.completed.value)

    print(f'Заказ {order.title} обработан')
