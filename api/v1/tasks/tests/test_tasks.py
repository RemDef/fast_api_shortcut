from datetime import datetime, timezone
from http import HTTPStatus
from unittest.mock import ANY, AsyncMock, patch
from uuid import uuid4

from common.errors import ErrorMessages
from tasks.dto import TaskDTO
from tests.factories import TaskFactory


class TestTasks:
    TASKS_URL = "/v1/tasks/"

    async def test_create_task_success(self, logged_in_client):
        task_id = uuid4()
        now = datetime.now(timezone.utc)
        task = TaskDTO(
            id=task_id,
            title="Купить молоко",
            description="2 литра",
            is_done=False,
            created_at=now,
            updated_at=now,
        )

        with patch(
            "api.v1.tasks.create.endpoint.create_task",
            new_callable=AsyncMock,
            return_value=task,
        ) as mocked_create_task:
            response = await logged_in_client.post(
                self.TASKS_URL,
                json={"title": "Купить молоко", "description": "2 литра"},
            )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "id": str(task_id),
            "title": "Купить молоко",
            "description": "2 литра",
            "is_done": False,
            "created_at": ANY,
            "updated_at": ANY,
        }
        mocked_create_task.assert_awaited_once()

    async def test_create_task_unauthorized(self, client):
        response = await client.post(
            self.TASKS_URL,
            json={"title": "Без токена", "description": None},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED

    async def test_get_tasks_paginated(self, db_session, user, logged_in_client):

        tasks = TaskFactory.build_batch(3, user_id=user.id)
        db_session.add_all(tasks)
        await db_session.commit()

        # 1
        response = await logged_in_client.get(
            f"{self.TASKS_URL}?limit=2&offset=0",
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
        response = await logged_in_client.get(
            f"{self.TASKS_URL}?limit=2&offset=2",
        )
        assert response.status_code == HTTPStatus.OK
        data = response.json()
        assert data["count"] == 3
        assert len(data["results"]) == 1
        assert data["next"] is None
        assert data["previous"] is not None
        assert "limit=2" in data["previous"]
        assert "offset=0" in data["previous"]

    async def test_update_task_success(self, logged_in_client):
        task_id = uuid4()
        now = datetime.now(timezone.utc)
        task = TaskDTO(
            id=task_id,
            title="Новое название",
            description=None,
            is_done=True,
            created_at=now,
            updated_at=now,
        )

        with patch(
            "api.v1.tasks.update.endpoint.update_task",
            new_callable=AsyncMock,
            return_value=task,
        ) as mocked_update_task:
            response = await logged_in_client.patch(
                f"{self.TASKS_URL}{task_id}",
                json={"title": "Новое название", "is_done": True},
            )

        assert response.status_code == HTTPStatus.OK
        assert response.json() == {
            "id": str(task_id),
            "title": "Новое название",
            "description": None,
            "is_done": True,
            "created_at": ANY,
            "updated_at": ANY,
        }
        mocked_update_task.assert_awaited_once()

    async def test_cannot_access_foreign_task(
        self, logged_in_client, other_auth_headers
    ):
        created = await logged_in_client.post(
            self.TASKS_URL, json={"title": "Чужая задача", "description": None}
        )
        task_id = created.json()["id"]

        response = await logged_in_client.get(
            f"{self.TASKS_URL}{task_id}",
            headers=other_auth_headers,
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"detail": ErrorMessages.TASK_NOT_FOUND}
