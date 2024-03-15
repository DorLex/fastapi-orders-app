import os

from dotenv import load_dotenv

from src.config import BASE_DIR

DOTENV_PATH_TEST = BASE_DIR / 'tests/.test.env'

load_dotenv(DOTENV_PATH_TEST)

DB_USER_TEST = os.getenv('POSTGRES_USER_TEST')
DB_PASS_TEST = os.getenv('POSTGRES_PASSWORD_TEST')
DB_HOST_TEST = os.getenv('POSTGRES_HOST_TEST')
DB_PORT_TEST = os.getenv('POSTGRES_PORT_TEST')
DB_NAME_TEST = os.getenv('POSTGRES_DB_TEST')

DATABASE_URL_TEST = f'postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

MODE = os.getenv('MODE')
