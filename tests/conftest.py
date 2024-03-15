import pytest
from starlette import status
from starlette.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.dependencies import get_db
from src.main import app
from .config import DATABASE_URL_TEST, MODE

engine_test = create_engine(DATABASE_URL_TEST)
SessionTest = sessionmaker(engine_test, autocommit=False, autoflush=False)


@pytest.fixture(scope='session', autouse=True)
def prepare_db():
    assert MODE == 'TEST'
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


@pytest.fixture(scope='session')
def base_test_user_data():
    return {
        'username': 'base_test_user',
        'password': '123456789',
    }


@pytest.fixture(scope='session')
def create_base_test_user(prepare_db, client, base_test_user_data):
    response = client.post('/register', json=base_test_user_data)
    assert response.status_code == status.HTTP_201_CREATED, response.text


@pytest.fixture(scope='session')
def access_token(create_base_test_user, client, base_test_user_data):
    response = client.post('/auth/token', data=base_test_user_data)
    assert response.status_code == status.HTTP_200_OK, response.text
    return response.json().get('access_token')


@pytest.fixture(scope='session')
def auth_headers(access_token):
    return {'Authorization': f'Bearer {access_token}'}
