from starlette import status


class TestUsers:
    def test_read_users(self, client, auth_headers):
        response = client.get('/users', headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK, response.text

    def test_read_users_me(self, client, auth_headers, base_test_user_data):
        response = client.get('/users/me/', headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK, response.text
        assert response.json().get('username') == base_test_user_data.get('username')
