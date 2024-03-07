from src.kafka_service.consumer.consumer import consumer
from src.order_processing.processing.processing import process_order


def run_consumer_listening():
    for message in consumer:
        process_order(message)
