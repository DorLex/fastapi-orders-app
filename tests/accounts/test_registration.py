from starlette import status

from src.accounts.service.crud import get_user_by_username
from tests.conftest import SessionTest


def test_registration(client):
    username = 'reg_user_1'
    reg_user_1 = {
        'username': username,
        'password': '123456789',
    }

    response = client.post('/register', json=reg_user_1)

    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert response.json().get('username') == username

    with SessionTest() as db:
        db_user = get_user_by_username(db, username)
        assert db_user.username == username
