from src.kafka_service.consumer.consumer import consumer

if __name__ == '__main__':

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
