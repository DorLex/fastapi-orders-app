from kafka import KafkaProducer

from src.kafka_service.config import KAFKA_BOOTSTRAP_SERVERS
from src.kafka_service.utils import serializer

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=serializer
)
