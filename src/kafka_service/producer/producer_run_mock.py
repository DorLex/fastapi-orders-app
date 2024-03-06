from time import sleep

from src.kafka_service.producer.producer import producer

if __name__ == '__main__':

    order_id = 1

    while True:
        message = {'order_id': order_id}

        producer.send('orders', message)
        print(f'Producer: Сообщение = {message}')

        sleep(2)
        order_id += 1

# docker compose exec app python -m src.kafka_service.producer.producer_run_mock
# docker compose exec app python -m src.run_consumer
