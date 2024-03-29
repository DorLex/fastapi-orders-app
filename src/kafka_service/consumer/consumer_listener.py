from src.kafka_service.consumer.consumer import get_consumer
from src.order_processing.processing.processing import run_order_processing


async def consumer_listening():
    consumer = await get_consumer()

    async with consumer as cs:
        async for message in cs:
            await run_order_processing(message)
