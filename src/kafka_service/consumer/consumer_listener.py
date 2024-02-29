from src.kafka_service.consumer.consumer import consumer


def run_consumer():
    for message in consumer:
        print(
            'Consumer:',
            f'{message.topic=}',
            f'{message.partition=}',
            f'{message.offset=}',
            f'{message.key=}',
            f'{message.value=}',
            sep='\n  '
        )
