from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from api.v1.users.response import UserResponse
from users.services import get_users

router = APIRouter()


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Получить пользователей",
    description="Получить список доступных пользователей.",
    response_description="Пользователи получены",
)
async def get_users_endpoint(
    session: AsyncSession = Depends(get_session),
) -> list[UserResponse]:
    users = await get_users(session=session)
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            birthdate=user.birthdate,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
        for user in users
    ]
