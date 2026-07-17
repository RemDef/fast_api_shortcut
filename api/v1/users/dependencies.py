from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from common.errors import ErrorMessages
from database import get_session
from users.exceptions import UserNotFoundError
from users.services import get_user_by_id
from users.models import User


async def get_user_or_404(
    user_id: str,
    session: AsyncSession = Depends(get_session),
) -> User:
    try:
        return await get_user_by_id(session, user_id=user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.USER_NOT_FOUND,
        )
