from fastapi import APIRouter, Depends, status, HTTPException

from api.v1.tasks.responses import TASK_NOT_FOUND_RESPONSES
from database import get_session
from tasks.services import delete_task
from users.models import User
from api.v1.auth.dependencies import get_current_user
from tasks.exceptions import TaskNotFoundError
from common.errors import ErrorMessages

router = APIRouter(responses=TASK_NOT_FOUND_RESPONSES)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу",
    description="Удаляет задачу текущего авторизованного пользователя.",
    response_description="Задача удалена",
)
async def delete_task_endpoint(
    task_id: str, user: User = Depends(get_current_user), session=Depends(get_session)
) -> None:
    try:
        await delete_task(session=session, task_id=task_id, user_id=user.id)
    except TaskNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.TASK_NOT_FOUND,
        )
