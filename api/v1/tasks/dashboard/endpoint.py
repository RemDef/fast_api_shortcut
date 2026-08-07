import asyncio

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import require_admin
from api.v1.tasks.active_users.response import ActiveUserItem
from api.v1.tasks.dashboard.response import TasksDashboardResponse
from api.v1.tasks.stats.by_day.response import TasksStatsByDayItem
from api.v1.tasks.stats.total.response import TasksStatsTotalResponse
from database import get_session
from tasks.services import (
    get_active_users,
    get_tasks_stats_by_day,
    get_tasks_stats_total,
)
from users.dto import UserDTO

router = APIRouter()


@router.get(
    "/dashboard",
    response_model=TasksDashboardResponse,
    summary="Дашборд задач",
    description="Общая статистика, по дням и активные пользователи "
    "(параллельно). Только админ.",
)
async def get_tasks_dashboard_endpoint(
    admin: UserDTO = Depends(require_admin),
    limit: int = Query(
        default=10, ge=1, le=100, description="Сколько активных пользователей вернуть"
    ),
    offset: int = Query(
        default=0, ge=0, description="Сколько активных пользователей пропустить"
    ),
    session_stats_total: AsyncSession = Depends(get_session, use_cache=False),
    session_stats_by_day: AsyncSession = Depends(get_session, use_cache=False),
    session_active_user: AsyncSession = Depends(get_session, use_cache=False),
) -> TasksDashboardResponse:
    total_data, by_day_data, active_data = await asyncio.gather(
        get_tasks_stats_total(session=session_stats_total, user_id=admin.id),
        get_tasks_stats_by_day(session=session_stats_by_day, user_id=admin.id),
        get_active_users(session=session_active_user, limit=limit, offset=offset),
    )

    return TasksDashboardResponse(
        total=TasksStatsTotalResponse.from_dto(dto=total_data),
        by_day=[TasksStatsByDayItem.from_dto(dto=row) for row in by_day_data],
        active_users=[ActiveUserItem.from_dto(dto=row) for row in active_data],
    )
