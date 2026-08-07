from http import HTTPStatus


class TestUsersAccess:
    async def test_users_list_forbidden_for_non_admin(self, client, auth_headers):
        response = await client.get("/v1/users/", headers=auth_headers)
        assert response.status_code == HTTPStatus.FORBIDDEN

    async def test_users_list_unauthorized(self, client):
        response = await client.get("/v1/users/")
        assert response.status_code == HTTPStatus.UNAUTHORIZED
