import json
from kafka import KafkaConsumer


def deserializer(mess):
    return json.loads(mess.decode('utf-8'))


consumer = KafkaConsumer(
    'messages',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    value_deserializer=deserializer
)

if __name__ == '__main__':

    for message in consumer:
        print(message.value)
