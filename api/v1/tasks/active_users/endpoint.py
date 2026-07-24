from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.active_users.response import ActiveUserItem
from database import get_session
from tasks.services import get_active_users

router = APIRouter()


@router.get(
    "/active-users",
    response_model=list[ActiveUserItem],
    summary="Активные пользователи",
    description="Топ пользователей по числу невыполненных задач.",
)
async def get_active_users_endpoint(
    limit: int = Query(
        default=10, ge=1, le=100, description="Сколько пользователей вернуть"
    ),
    _: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[ActiveUserItem]:
    rows = await get_active_users(session=session, limit=limit)
    return [ActiveUserItem(**row) for row in rows]
