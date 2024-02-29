from time import sleep

from src.kafka_service.producer.producer import producer

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

# docker compose exec app python -m src.kafka_service.producer.producer_run_mock
# docker compose exec app python -m src.run_consumer
