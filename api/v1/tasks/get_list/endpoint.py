from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Literal

from api.v1.tasks.create.response import TaskResponse
from api.v1.auth.dependencies import get_current_user
from database import get_session
from tasks.services import get_tasks
from users.models import User

router = APIRouter()


@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="Получить список задач",
    description="Получает список задач текущего авторизованного пользователя.",
    response_description="Задачи получены",
)
async def get_tasks_endpoint(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    limit: int = Query(default=20, ge=1, le=100, description="Сколько задач вернуть"),
    offset: int = Query(default=0, ge=0, description="Сколько задач пропустить"),
    is_done: bool | None = Query(
        default=None,
        description="Фильтр по статусу: true — выполненные, false — активные",
    ),
    created_from: datetime | None = Query(
        default=None,
        description="Задачи, созданные не раньше этой даты",
    ),
    created_to: datetime | None = Query(
        default=None,
        description="Задачи, созданные не позже этой даты",
    ),
    order_by: Literal["created_at", "updated_at", "title"] = Query(
        default="created_at",
        description="Поле для сортировки",
    ),
    direction: Literal["asc", "desc"] = Query(
        default="desc",
        description="Направление сортировки",
    ),
    search: str | None = Query(
        default=None,
        alias="query",
        min_length=1,
        max_length=100,
        description="Поиск по подстроке в названии и описании",
    ),
) -> list[TaskResponse]:
    tasks = await get_tasks(
        session=session,
        user_id=user.id,
        limit=limit,
        offset=offset,
        is_done=is_done,
        created_from=created_from,
        created_to=created_to,
        order_by=order_by,
        direction=direction,
        search=search,
    )
    return [
        TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            is_done=task.is_done,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        for task in tasks
    ]
