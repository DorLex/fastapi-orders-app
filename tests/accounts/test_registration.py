from fastapi import FastAPI
from httpx import AsyncClient
from starlette import status

from src.accounts.models import UserModel
from src.accounts.repositories.user import UserRepository
from tests.conftest import SessionTest


async def test_registration(app: FastAPI, client: AsyncClient):
    username = 'registered_user_1'
    reg_user_1 = {
        'username': username,
        'email': 'registered-user-1@test.com',
        'password': '123456789',
    }

    url = app.url_path_for('user_registration')
    response = await client.post(url, json=reg_user_1)

    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert response.json().get('username') == username

    async with SessionTest() as db:
        db_user: UserModel = await UserRepository(db).get_by_username(username)
        assert db_user.username == username
