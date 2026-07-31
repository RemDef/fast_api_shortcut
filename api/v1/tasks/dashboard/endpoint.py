import asyncio

from fastapi import APIRouter, Depends

from api.v1.auth.dependencies import require_admin
from api.v1.tasks.active_users.response import ActiveUserItem
from api.v1.tasks.dashboard.response import TasksDashboardResponse
from api.v1.tasks.stats.by_day.response import TasksStatsByDayItem
from api.v1.tasks.stats.total.response import TasksStatsTotalResponse
from database import db_helper
from tasks.dto import ActiveUserDTO, TasksStatsByDayDTO, TasksStatsTotalDTO
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
) -> TasksDashboardResponse:
    async def fetch_total() -> TasksStatsTotalDTO:
        async with db_helper.session_factory() as session:
            return await get_tasks_stats_total(session=session, user_id=admin.id)

    async def fetch_by_day() -> list[TasksStatsByDayDTO]:
        async with db_helper.session_factory() as session:
            return await get_tasks_stats_by_day(session=session, user_id=admin.id)

    async def fetch_active_users() -> list[ActiveUserDTO]:
        async with db_helper.session_factory() as session:
            return await get_active_users(session=session, limit=10, offset=0)

    total_data, by_day_data, active_data = await asyncio.gather(
        fetch_total(),
        fetch_by_day(),
        fetch_active_users(),
    )

    return TasksDashboardResponse(
        total=TasksStatsTotalResponse.from_dto(dto=total_data),
        by_day=[TasksStatsByDayItem.from_dto(dto=row) for row in by_day_data],
        active_users=[ActiveUserItem.from_dto(dto=row) for row in active_data],
    )
