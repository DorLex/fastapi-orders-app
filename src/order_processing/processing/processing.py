from aiokafka import ConsumerRecord

from src.order_processing.notification import send_notification
from src.order_processing.processing.logic import execute_order


def process_order(consumer_message: ConsumerRecord):
    order_id = consumer_message.value.get('order_id')

    try:
        execute_order(order_id)
        send_notification(f'Заказ №{order_id} успешно обработан.')
    except Exception as ex:
        send_notification(f'Произошла ошибка при обработке Заказа №{order_id}')
        print(f'<Exception: {ex}>')
