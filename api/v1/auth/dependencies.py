from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from common.auth import get_user_id_from_token
from common.errors import ErrorMessages
from database import get_session
from users.dto import UserDTO
from users.exceptions import UserNotFoundError
from users.services import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/login")


async def get_current_user_model(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> UserDTO:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorMessages.INVALID_TOKEN,
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_uuid = get_user_id_from_token(token)
    if user_uuid is None:
        raise credentials_exception

    try:
        return await get_user_by_id(session=session, user_id=user_uuid)
    except UserNotFoundError:
        raise credentials_exception


async def get_current_user(
    user: UserDTO = Depends(get_current_user_model),
) -> UUID:
    return user.id


async def require_admin(
    user: UserDTO = Depends(get_current_user_model),
) -> UserDTO:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав",
        )
    return user
