from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import require_admin
from api.v1.users.common.schemas import UserResponse
from api.v1.users.responses import USER_NOT_FOUND_RESPONSES
from common.errors import ErrorMessages
from database import get_session
from users.dto import UserDTO
from users.exceptions import UserNotFoundError
from users.services import get_user_by_id

router = APIRouter(responses=USER_NOT_FOUND_RESPONSES)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Получить пользователя",
    description="Получить данные пользователя по id (только для админа).",
    response_description="Пользователь получен",
)
async def get_user_endpoint(
    user_id: str,
    _: UserDTO = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    try:
        user = await get_user_by_id(session, user_id=user_id)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessages.USER_NOT_FOUND,
        )
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        birthdate=user.birthdate,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )
