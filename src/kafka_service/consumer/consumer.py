import json
from kafka import KafkaConsumer

from src.kafka_service.config import KAFKA_BOOTSTRAP_SERVERS


def deserializer(mess):
    return json.loads(mess.decode('utf-8'))


consumer = KafkaConsumer(
    'messages',
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    auto_offset_reset='earliest',
    value_deserializer=deserializer
)

if __name__ == '__main__':

    for message in consumer:
        print(f'Consumer: {message.value}')
