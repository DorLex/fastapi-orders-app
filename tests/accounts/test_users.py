from starlette import status


class TestUsers:
    def test_read_users(self, client, auth_headers):
        response = client.get('/users', headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
