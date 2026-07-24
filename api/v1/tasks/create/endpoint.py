from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.common.schemas import TaskResponse
from api.v1.tasks.create.request import CreateTaskRequest
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
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    task = await create_task(
        session=session,
        user_id=user_id,
        title=body.title,
        description=body.description,
    )
    return TaskResponse.from_dto(dto=task)
