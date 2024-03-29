from aiokafka import ConsumerRecord

from src.database import SessionLocal
from src.order_processing.notification import send_notification
from src.order_processing.processing.logic import execute_order
from src.order_processing.service import OrderProcessingService


async def run_order_processing(consumer_message: ConsumerRecord):
    order_id = consumer_message.value.get('order_id')

    with SessionLocal() as db:
        order_processing_service = OrderProcessingService(db)

        await order_processing_service.execute_order(order_id)

        # try:
        #     execute_order(order_id)
        #     # send_notification(f'Заказ №{order_id} успешно обработан.')
        # except Exception as ex:
        #     # send_notification(f'Произошла ошибка при обработке Заказа №{order_id}')
        #     print(f'<Exception: {ex}>')
