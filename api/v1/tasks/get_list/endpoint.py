from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.tasks.create.response import TaskResponse
from api.v1.auth.dependencies import get_current_user
from database import get_session
from tasks.services import get_tasks
from users.models import User

router = APIRouter()


@router.get("/", response_model=list[TaskResponse])
async def get_tasks_endpoint(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[TaskResponse]:
    tasks = await get_tasks(session=session, user_id=user.id)
    return [
        TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            is_done=task.is_done,
            created_at=task.created_at,
            updated_at=task.updated_at,
        )
        for task in tasks
    ]
