from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.tasks.create.response import TaskResponse
from api.v1.tasks.update.request import UpdateTaskRequest
from api.v1.auth.dependencies import get_current_user
from tasks.services import update_task
from database import get_session
from users.models import User

router = APIRouter()


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task_endpoint(
    task_id: str,
    body: UpdateTaskRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:

    task = await update_task(
        session=session,
        task_id=task_id,
        user_id=user.id,
        title=body.title,
        description=body.description,
        is_done=body.is_done,
    )
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
