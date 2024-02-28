from time import sleep

from sqlalchemy.orm import Session

from src.orders.enums import OrderStatusEnum
from src.orders.models import OrderModel
from src.orders.service.crud import update_order_status


def order_processing(db: Session, order: OrderModel):
    print(f'Начало обработки заказа {order.title}')
    sleep(5)

    updated_order = update_order_status(db, order, OrderStatusEnum.completed.value)

    print(f'Заказ {updated_order.title} пользователя {updated_order.owner_id} обработан')
