from httpx import AsyncClient
from starlette import status


async def test_login_by_access_token(client: AsyncClient):
    user_data = {
        'username': 'test_user_for_auth',
        'email': 'test-user-for-auth@test.com',
        'password': '123456789',
    }

    await client.post('/registration/', json=user_data)

    response = await client.post('/auth/token/', data=user_data)

    assert response.status_code == status.HTTP_200_OK, response.text
