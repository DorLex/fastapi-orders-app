import json
from time import sleep

from kafka import KafkaProducer

from src.kafka_service.config import KAFKA_BOOTSTRAP_SERVERS


def serializer(mess):
    return json.dumps(mess).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=serializer
)

if __name__ == '__main__':

    user_id = 1

    while True:
        message = {
            'user_id': user_id,
            'message': str(user_id) * 10
        }

        producer.send('messages', message)
        print(f'Producer: Сообщение = {message}')

        sleep(2)
        user_id += 1

# docker compose exec app python -m src.kafka_service.producer.producer
# docker compose exec app python -m src.kafka_service.consumer.consumer
