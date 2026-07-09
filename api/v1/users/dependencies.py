from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.errors import ErrorMessages
from database import get_session
from users.models import User


async def get_user_or_404(
    user_id: str,
    session: AsyncSession = Depends(get_session),
) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail=ErrorMessages.USER_NOT_FOUND)
    return user
