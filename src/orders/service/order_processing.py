from time import sleep

from src.orders.enums import OrderStatusEnum
from src.orders.service.crud import update_order_status


def order_processing(order_id: int):
    print(f'<Начало обработки заказа №{order_id}>')
    sleep(3)

    update_order_status(order_id, OrderStatusEnum.completed.value)
