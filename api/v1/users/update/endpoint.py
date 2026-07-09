from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.users.response import UserResponse
from api.v1.users.update.request import UpdateUserRequest
from database import get_session
from users.services import update_user

router = APIRouter()


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user_endpoint(
    user_id: str,
    body: UpdateUserRequest,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    user = await update_user(
        session=session,
        user_id=user_id,
        username=body.username,
        email=body.email,
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
