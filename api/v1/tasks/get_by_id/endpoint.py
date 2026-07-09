from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.tasks.create.response import TaskResponse
from api.v1.auth.dependencies import get_current_user
from database import get_session
from tasks.services import get_task_by_id
from users.models import User

router = APIRouter()


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_endpoint(
    task_id: str,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TaskResponse:
    task = await get_task_by_id(session, task_id=task_id, user_id=user.id)
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        is_done=task.is_done,
        created_at=task.created_at,
        updated_at=task.updated_at,
    )
