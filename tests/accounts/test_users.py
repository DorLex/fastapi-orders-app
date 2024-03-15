from starlette import status


class TestUsers:
    def test_read_users(self, client):
        response = client.get('/users')
        assert response.status_code == status.HTTP_200_OK
        # assert response.json() == [{'username': 'alex', 'id': 1}]
