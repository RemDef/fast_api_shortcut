from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.common.schemas import TaskResponse
from api.v1.tasks.responses import TASK_NOT_FOUND_RESPONSES
from common.errors import ErrorMessages
from database import get_session
from tasks.exceptions import TaskNotFoundError
from tasks.services import get_task_by_id

router = APIRouter(responses=TASK_NOT_FOUND_RESPONSES)


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Получить задачу пользователя по id",
    description="Получает задачу текущего авторизованного пользователя по id.",
    response_description="Задача получена",
)
async def get_task_endpoint(
    task_id: str,
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    try:
        task = await get_task_by_id(session, task_id=task_id, user_id=user_id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.TASK_NOT_FOUND,
        )
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
