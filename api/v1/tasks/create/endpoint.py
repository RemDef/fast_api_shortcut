from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.common.schemas import TaskResponse
from api.v1.tasks.create.request import CreateTaskRequest
from cache.backend import RedisCacheBackend
from cache.dependencies import get_cache
from database import get_session
from tasks.cache_keys import tasks_list_pattern
from tasks.services import create_task

router = APIRouter()


@router.post(
    "/",
    response_model=TaskResponse,
    summary="Создать задачу",
    description="Создаёт новую задачу для текущего авторизованного пользователя.",
    response_description="Задача создана",
)
async def create_task_endpoint(
    body: CreateTaskRequest,
    user_id: UUID = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
    cache: RedisCacheBackend = Depends(get_cache),
) -> TaskResponse:
    task = await create_task(
        session=session,
        user_id=user_id,
        title=body.title,
        description=body.description,
    )
    await cache.delete_pattern(tasks_list_pattern(user_id))
    return TaskResponse.from_dto(dto=task)
