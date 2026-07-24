from fastapi import APIRouter, Depends

from api.v1.users.common.schemas import UserResponse
from api.v1.users.dependencies import get_user_or_404
from api.v1.users.responses import USER_NOT_FOUND_RESPONSES
from users.models import User

router = APIRouter(responses=USER_NOT_FOUND_RESPONSES)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Получить пользователя",
    description="Получить данные пользователя по id.",
    response_description="Пользователь получен",
)
async def get_user_endpoint(
    user: User = Depends(get_user_or_404),
) -> UserResponse:
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
