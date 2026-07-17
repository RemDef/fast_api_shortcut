from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.users.register.request import RegisterUserRequest
from api.v1.users.response import UserResponse
from database import get_session
from users.services import register_user
from users.dto import RegisterUserDTO

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Зарегистрировать пользователя",
    description="Зарегистрировать нового пользователя.",
    response_description="Пользователь зарегистрирован",
)
async def register_user_endpoint(
    body: RegisterUserRequest,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    data = RegisterUserDTO(
        username=body.username,
        email=body.email,
        password=body.password.get_secret_value(),
        first_name=body.first_name,
        last_name=body.last_name,
        birthdate=body.birthdate,
    )
    user = await register_user(session=session, data=data)

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
