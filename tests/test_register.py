from http import HTTPStatus

REGISTER_URL = "/v1/users/register"

VALID_USER = {
    "username": "test_user",
    "email": "test_user@example.com",
    "password": "Qwerty1!",
    "first_name": "Тест",
    "last_name": "Тестов",
    "birthdate": "1995-01-15",
}


class TestRegister:
    async def test_register_user_success(self, client):
        response = await client.post(REGISTER_URL, json=VALID_USER)

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data["username"] == "test_user"
        assert data["email"] == "test_user@example.com"
        assert "id" in data
        assert set(data.keys()) == {
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "birthdate",
        }

    async def test_login_after_register(self, client):
        await client.post(REGISTER_URL, json=VALID_USER)

        response = await client.post(
            "/v1/auth/login",
            data={
                "username": VALID_USER["username"],
                "password": VALID_USER["password"],
            },
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["token_type"] == "bearer"
        assert set(data.keys()) == {"access_token", "token_type"}
