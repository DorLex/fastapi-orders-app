from starlette import status


def test_login_for_access_token(client):
    user_data = {
        'username': 'test_user_for_auth',
        'email': 'test-user-for-auth@test.com',
        'password': '123456789',
    }

    client.post('/register', json=user_data)
    response = client.post('/auth/token', data=user_data)

    assert response.status_code == status.HTTP_200_OK, response.text
