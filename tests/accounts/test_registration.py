from starlette import status

from src.accounts.models import UserModel
from src.accounts.repositories.user import UserRepository
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
        db_user: UserModel = UserRepository(db).get_by_username(username)
        assert db_user.username == username
