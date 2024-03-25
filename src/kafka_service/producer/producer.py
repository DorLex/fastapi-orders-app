from aiokafka import AIOKafkaProducer

from src.kafka_service.config import KAFKA_BOOTSTRAP_SERVERS
from src.kafka_service.utils import serializer


async def get_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=serializer
    )

    return producer
