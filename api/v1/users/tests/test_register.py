from datetime import date
from http import HTTPStatus
from types import SimpleNamespace
from unittest.mock import ANY, AsyncMock, patch
from uuid import uuid4


class TestRegister:
    REGISTER_URL = "/v1/users/register"

    REQUEST_USER = {
        "username": "test_user",
        "email": "test_user@example.com",
        "password": "Qwerty1!",
        "first_name": "Тест",
        "last_name": "Тестов",
        "birthdate": "1995-01-15",
    }

    async def test_register_user_success(self, client):
        """Интеграционный: реальный service + БД (smoke)."""
        response = await client.post(self.REGISTER_URL, json=self.REQUEST_USER)

        assert response.status_code == HTTPStatus.CREATED
        data = response.json()
        assert data == {
            "id": ANY,
            "username": self.REQUEST_USER["username"],
            "email": self.REQUEST_USER["email"],
            "first_name": self.REQUEST_USER["first_name"],
            "last_name": self.REQUEST_USER["last_name"],
            "birthdate": self.REQUEST_USER["birthdate"],
        }

    async def test_register_user_success_mocks_service(self, client):
        """API-тест: бизнес-логику мокаем, проверяем только endpoint."""
        fake_user = SimpleNamespace(
            id=uuid4(),
            username=self.REQUEST_USER["username"],
            email=self.REQUEST_USER["email"],
            first_name=self.REQUEST_USER["first_name"],
            last_name=self.REQUEST_USER["last_name"],
            birthdate=date(1995, 1, 15),
        )

        with patch(
            "api.v1.users.register.endpoint.register_user",
            new_callable=AsyncMock,
            return_value=fake_user,
        ) as mocked_register:
            response = await client.post(self.REGISTER_URL, json=self.REQUEST_USER)

        assert response.status_code == HTTPStatus.CREATED
        assert response.json() == {
            "id": str(fake_user.id),
            "username": self.REQUEST_USER["username"],
            "email": self.REQUEST_USER["email"],
            "first_name": self.REQUEST_USER["first_name"],
            "last_name": self.REQUEST_USER["last_name"],
            "birthdate": self.REQUEST_USER["birthdate"],
        }
        mocked_register.assert_awaited_once()
