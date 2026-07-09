from fastapi import APIRouter, Depends, status

from database import get_session
from tasks.services import delete_task
from users.models import User
from api.v1.auth.dependencies import get_current_user

router = APIRouter()


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(
    task_id: str, user: User = Depends(get_current_user), session=Depends(get_session)
) -> None:
    await delete_task(session=session, task_id=task_id, user_id=user.id)
