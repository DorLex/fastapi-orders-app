from httpx import AsyncClient
from starlette import status


class TestUsers:
    async def test_read_users(self, client: AsyncClient, auth_headers):
        response = await client.get('/users/', headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        assert len(response.json()) > 0

    async def test_read_users_me(self, client: AsyncClient, auth_headers, base_test_user_data):
        response = await client.get('/users/me/', headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json().get('username') == base_test_user_data.get('username')
