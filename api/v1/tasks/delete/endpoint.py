from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.responses import TASK_NOT_FOUND_RESPONSES
from cache.backend import RedisCacheBackend
from cache.dependencies import get_cache
from common.errors import ErrorMessages
from database import get_session
from tasks.cache_keys import tasks_list_pattern
from tasks.exceptions import TaskNotFoundError
from tasks.services import delete_task

router = APIRouter(responses=TASK_NOT_FOUND_RESPONSES)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу",
    description="Удаляет задачу текущего авторизованного пользователя.",
    response_description="Задача удалена",
)
async def delete_task_endpoint(
    task_id: UUID,
    user_id: UUID = Depends(get_current_user),
    session=Depends(get_session),
    cache: RedisCacheBackend = Depends(get_cache),
) -> None:
    try:
        await delete_task(session=session, task_id=task_id, user_id=user_id)
        await cache.delete_pattern(tasks_list_pattern(user_id))
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.TASK_NOT_FOUND,
        )
