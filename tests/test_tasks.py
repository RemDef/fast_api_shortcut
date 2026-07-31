import pytest

TASKS_URL = "/v1/tasks/"


@pytest.mark.asyncio
async def test_create_task_success(client, auth_headers):
    response = await client.post(
        TASKS_URL,
        json={"title": "Купить молоко", "description": "2 литра"},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Купить молоко"
    assert data["description"] == "2 литра"
    assert data["is_done"] is False
    assert "id" in data


@pytest.mark.asyncio
async def test_create_task_unauthorized(client):
    response = await client.post(
        TASKS_URL,
        json={"title": "Без токена", "description": None},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_tasks_paginated(client, auth_headers):
    await client.post(
        TASKS_URL,
        json={"title": "Задача один", "description": None},
        headers=auth_headers,
    )
    await client.post(
        TASKS_URL,
        json={"title": "Задача два", "description": None},
        headers=auth_headers,
    )

    response = await client.get(TASKS_URL, headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert len(data["results"]) == 2
    assert "next" in data
    assert "previous" in data


@pytest.mark.asyncio
async def test_update_task_success(client, auth_headers):
    created = await client.post(
        TASKS_URL,
        json={"title": "Старое название", "description": None},
        headers=auth_headers,
    )
    task_id = created.json()["id"]

    response = await client.patch(
        f"{TASKS_URL}{task_id}",
        json={"title": "Новое название", "is_done": True},
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Новое название"
    assert data["is_done"] is True


@pytest.mark.asyncio
async def test_cannot_access_foreign_task(client, auth_headers):
    created = await client.post(
        TASKS_URL,
        json={"title": "Чужая задача", "description": None},
        headers=auth_headers,
    )
    task_id = created.json()["id"]

    other = {
        "username": "other_user",
        "email": "other@example.com",
        "password": "Qwerty1!",
        "first_name": "Other",
        "last_name": "User",
        "birthdate": "1990-05-05",
    }
    await client.post("/v1/users/register", json=other)
    login = await client.post(
        "/v1/auth/login",
        data={"username": other["username"], "password": other["password"]},
    )
    other_headers = {"Authorization": f"Bearer {login.json()['access_token']}"}

    response = await client.get(f"{TASKS_URL}{task_id}", headers=other_headers)

    assert response.status_code == 404
