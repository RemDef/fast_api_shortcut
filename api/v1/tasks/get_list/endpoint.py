from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.common.schemas import TaskResponse
from api.v1.tasks.get_list.request import TaskQuery
from database import get_session
from tasks.services import get_tasks

router = APIRouter()


@router.get(
    "/",
    response_model=list[TaskResponse],
    summary="Получить список задач",
    description="Получает список задач текущего авторизованного пользователя.",
    response_description="Задачи получены",
)
async def get_tasks_endpoint(
    query: Annotated[TaskQuery, Query()],
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[TaskResponse]:
    tasks = await get_tasks(
        session=session,
        user_id=user_id,
        limit=query.limit,
        offset=query.offset,
        is_done=query.is_done,
        created_from=query.created_from,
        created_to=query.created_to,
        order_by=query.order_by,
        direction=query.direction,
        search=query.search,
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
