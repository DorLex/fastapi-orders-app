from src.kafka_service.consumer.consumer import consumer
from src.orders.service.notification import send_notification, send_bad_notification
from src.orders.service.order_processing import order_processing


def run_consumer():
    for message in consumer:
        # print(
        #     'Consumer:',
        #     f'{message.topic=}',
        #     f'{message.partition=}',
        #     f'{message.offset=}',
        #     f'{message.key=}',
        #     f'{message.value=}',
        #     sep='\n  '
        # )

        order_id = message.value.get('order_id')

        try:
            order_processing(order_id)
        except Exception as ex:
            send_bad_notification(order_id)
            print('Exception:', ex)
        else:
            send_notification(order_id)
