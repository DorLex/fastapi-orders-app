import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from .config import DATABASE_URL_TEST

engine_test = create_engine(DATABASE_URL_TEST)
SessionTest = sessionmaker(engine_test, autocommit=False, autoflush=False)


@pytest.fixture(scope='session')
def client():
    return TestClient(app=app)
