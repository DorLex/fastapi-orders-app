import os

from dotenv import load_dotenv

from src.config import DOTENV_PATH

load_dotenv(DOTENV_PATH)

KAFKA_HOST = os.getenv('KAFKA_HOST')
KAFKA_PORT = os.getenv('KAFKA_PORT')

KAFKA_BOOTSTRAP_SERVERS = f'{KAFKA_HOST}:{KAFKA_PORT}'
