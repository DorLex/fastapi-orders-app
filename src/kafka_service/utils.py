import json


def serializer(message):
    return json.dumps(message).encode('utf-8')


def deserializer(message):
    return json.loads(message.decode('utf-8'))
