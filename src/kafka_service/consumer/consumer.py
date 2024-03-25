from aiokafka import AIOKafkaConsumer

from src.kafka_service.config import KAFKA_BOOTSTRAP_SERVERS
from src.kafka_service.utils import deserializer


async def get_consumer():
    consumer = AIOKafkaConsumer(
        'orders',
        group_id='orders_group',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=deserializer
    )

    return consumer
