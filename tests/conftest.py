import pytest
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.dependencies import get_db
from src.main import app
from .config import DATABASE_URL_TEST

engine_test = create_engine(DATABASE_URL_TEST)
SessionTest = sessionmaker(engine_test, autocommit=False, autoflush=False)


@pytest.fixture(scope='session', autouse=True)
def prepare_db():
    Base.metadata.create_all(bind=engine_test)
    yield
    Base.metadata.drop_all(bind=engine_test)


def override_get_db():
    with SessionTest() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='session')
def client():
    return TestClient(app=app)
