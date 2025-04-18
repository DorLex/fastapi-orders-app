from aiokafka import ConsumerRecord

from src.database import SessionLocal
from src.order_processing.service import OrderProcessingService


async def run_order_processing(consumer_message: ConsumerRecord):
    order_id = consumer_message.value.get('order_id')
    customer_email = consumer_message.value.get('customer_email')

    async with SessionLocal() as session:
        order_processing_service = OrderProcessingService(session)
        await order_processing_service.execute_order(order_id, customer_email)
