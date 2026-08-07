from http import HTTPStatus

from common.errors import ErrorMessages
from tests.factories import TaskFactory

TASKS_URL = "/v1/tasks/"


class TestTasks:
    async def test_create_task_success(self, client, auth_headers):
        response = await client.post(
            TASKS_URL,
            json={"title": "Купить молоко", "description": "2 литра"},
            headers=auth_headers,
        )

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["title"] == "Купить молоко"
        assert data["description"] == "2 литра"
        assert data["is_done"] is False
        assert "id" in data

    async def test_create_task_unauthorized(self, client):
        response = await client.post(
            TASKS_URL,
            json={"title": "Без токена", "description": None},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_get_tasks_paginated(self, client, db_session, user, auth_headers):

        for _ in range(3):
            db_session.add(TaskFactory.build(user_id=user.id))
        await db_session.commit()

        # 1
        response = await client.get(
            f"{TASKS_URL}?limit=2&offset=0",
            headers=auth_headers,
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["count"] == 3
        assert len(data["results"]) == 2
        assert data["previous"] is None
        assert data["next"] is not None
        assert "limit=2" in data["next"]
        assert "offset=2" in data["next"]

        # 2
        response = await client.get(
            f"{TASKS_URL}?limit=2&offset=2",
            headers=auth_headers,
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["count"] == 3
        assert len(data["results"]) == 1
        assert data["next"] is None
        assert data["previous"] is not None
        assert "limit=2" in data["previous"]
        assert "offset=0" in data["previous"]

    async def test_update_task_success(self, client, auth_headers):
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

        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["title"] == "Новое название"
        assert data["is_done"] is True

    async def test_cannot_access_foreign_task(self, client, auth_headers):
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
        data = response.json()

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert data == {"detail": ErrorMessages.TASK_NOT_FOUND}
