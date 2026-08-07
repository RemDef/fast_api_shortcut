from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.common.schemas import TaskResponse
from api.v1.tasks.responses import TASK_NOT_FOUND_RESPONSES
from api.v1.tasks.update.request import UpdateTaskRequest
from cache.backend import RedisCacheBackend
from cache.dependencies import get_cache
from common.errors import ErrorMessages
from database import get_session
from tasks.cache_keys import tasks_list_pattern
from tasks.exceptions import TaskNotFoundError
from tasks.services import UNSET, update_task

router = APIRouter(responses=TASK_NOT_FOUND_RESPONSES)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Обновить задачу",
    description="Обновляет задачу текущего авторизованного пользователя.",
    response_description="Задача обновлена",
)
async def update_task_endpoint(
    task_id: UUID,
    body: UpdateTaskRequest,
    user_id: UUID = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    cache: RedisCacheBackend = Depends(get_cache),
) -> TaskResponse:

    try:
        updates = body.model_dump(exclude_unset=True)
        task = await update_task(
            session=session,
            task_id=task_id,
            user_id=user_id,
            title=updates.get("title", UNSET),
            description=updates.get("description", UNSET),
            is_done=updates.get("is_done", UNSET),
        )
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.TASK_NOT_FOUND,
        )

    await cache.delete_pattern(tasks_list_pattern(user_id))
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
