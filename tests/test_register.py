import pytest

REGISTER_URL = "/v1/users/register"

VALID_USER = {
    "username": "test_user",
    "email": "test_user@example.com",
    "password": "Qwerty1!",
    "first_name": "Тест",
    "last_name": "Тестов",
    "birthdate": "1995-01-15",
}


@pytest.mark.asyncio
async def test_register_user_success(client):
    response = await client.post(REGISTER_URL, json=VALID_USER)

    assert response.status_code == 201

    data = response.json()
    assert data["username"] == "test_user"
    assert data["email"] == "test_user@example.com"
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_login_after_register(client):
    await client.post(REGISTER_URL, json=VALID_USER)

    response = await client.post(
        "/v1/auth/login",
        data={
            "username": VALID_USER["username"],
            "password": VALID_USER["password"],
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
