from kafka import KafkaConsumer

from src.kafka_service.config import KAFKA_BOOTSTRAP_SERVERS
from src.kafka_service.utils import deserializer

consumer = KafkaConsumer(
    'messages',
    # group_id='my-group',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=deserializer
)
