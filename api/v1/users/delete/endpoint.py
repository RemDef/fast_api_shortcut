from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.users.responses import USER_NOT_FOUND_RESPONSES
from common.errors import ErrorMessages
from database import get_session
from users.exceptions import UserNotFoundError
from users.services import delete_user

router = APIRouter(responses=USER_NOT_FOUND_RESPONSES)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя",
    description="Удаляет пользователя с сервиса.",
    response_description="Пользователь удален",
)
async def delete_user_endpoint(
    user_id: str,
    session: AsyncSession = Depends(get_session),
) -> None:
    try:
        await delete_user(session=session, user_id=user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.USER_NOT_FOUND,
        )
