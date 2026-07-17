from fastapi import APIRouter, Depends
from api.v1.tasks.create.request import CreateTaskRequest
from api.v1.tasks.create.response import TaskResponse
from api.v1.auth.dependencies import get_current_user
from users.models import User
from database import get_session

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
    user: User = Depends(get_current_user),
    session=Depends(get_session),
) -> TaskResponse:
    task = await create_task(
        session=session,
        user_id=user.id,
        title=body.title,
        description=body.description,
    )
    return TaskResponse(
        id=task.id,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
