from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.accounts.schemas.user import UserOutSchema
from src.database import Base
from src.dependencies import get_db
from src.main import app
from .config import MODE, async_engine_test, SessionTest


@pytest.fixture(scope='session', autouse=True)
async def prepare_db():
    assert MODE == 'TEST'

    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with async_engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionTest() as db:
        yield db


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope='session')
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client


@pytest.fixture(scope='session')
async def base_test_user_data():
    return {
        'username': 'base_test_user',
        'email': 'base-test-user@test.com',
        'password': '123456789',
    }


@pytest.fixture(scope='session')
async def base_test_user(prepare_db, client: AsyncClient, base_test_user_data):
    response = await client.post('/registration/', json=base_test_user_data)
    assert response.status_code == status.HTTP_201_CREATED, response.text
    return UserOutSchema(**response.json())


@pytest.fixture(scope='session')
async def access_token(base_test_user, client: AsyncClient, base_test_user_data):
    response = await client.post('/auth/token/', data=base_test_user_data)
    assert response.status_code == status.HTTP_200_OK, response.text
    return response.json().get('access_token')


@pytest.fixture(scope='session')
async def auth_headers(access_token):
    return {'Authorization': f'Bearer {access_token}'}
