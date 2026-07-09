from fastapi import APIRouter, Depends
from api.v1.users.response import UserResponse
from users.models import User
from api.v1.users.dependencies import get_user_or_404

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse)
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
