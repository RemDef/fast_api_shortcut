from http import HTTPStatus
from unittest.mock import ANY


class TestLogin:
    REGISTER_URL = "/v1/users/register"
    LOGIN_URL = "/v1/auth/login"

    REQUEST_USER = {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "Qwerty1!",
        "first_name": "Тест",
        "last_name": "Тестов",
        "birthdate": "1995-01-15",
    }

    async def test_login_after_register(self, client):
        await client.post(self.REGISTER_URL, json=self.REQUEST_USER)

        response = await client.post(
            self.LOGIN_URL,
            data={
                "username": self.REQUEST_USER["username"],
                "password": self.REQUEST_USER["password"],
            },
        )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "access_token": ANY,
            "token_type": "bearer",
        }
