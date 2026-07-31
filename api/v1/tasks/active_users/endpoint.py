from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import require_admin
from api.v1.tasks.active_users.response import ActiveUserItem
from database import get_session
from tasks.services import get_active_users
from users.dto import UserDTO

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
    offset: int = Query(
        default=0, ge=0, description="Сколько пользователей пропустить"
    ),
    _: UserDTO = Depends(require_admin),
    session: AsyncSession = Depends(get_session),
) -> list[ActiveUserItem]:
    rows = await get_active_users(session=session, limit=limit, offset=offset)
    return [ActiveUserItem.from_dto(dto=row) for row in rows]
