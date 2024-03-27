import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

MODE = os.getenv('MODE')

DB_USER_TEST = os.getenv('POSTGRES_USER')
DB_PASS_TEST = os.getenv('POSTGRES_PASSWORD')
DB_HOST_TEST = os.getenv('POSTGRES_HOST')
DB_PORT_TEST = os.getenv('POSTGRES_PORT')
DB_NAME_TEST = os.getenv('POSTGRES_DB')

DATABASE_URL_TEST = f'postgresql+psycopg2://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

engine_test = create_engine(DATABASE_URL_TEST)
SessionTest = sessionmaker(engine_test, autocommit=False, autoflush=False)
