import json

from time import sleep

from kafka import KafkaProducer


def serializer(mess):
    return json.dumps(mess).encode('utf-8')


producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=serializer
)

if __name__ == '__main__':

    user_id = 1

    while True:
        message = {
            'user_id': user_id,
            'message': str(user_id) * 10
        }

        # Send it to our 'messages' topic
        producer.send('messages', message)
        print(f'Сообщение = {message}')

        sleep(2)
        user_id += 1

# kafka-topics.sh --bootstrap-server=localhost:9092 --list
# kafka-topics.sh --create --topic messages --bootstrap-server localhost:9092
