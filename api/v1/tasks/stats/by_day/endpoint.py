from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.stats.by_day.response import TasksStatsByDayItem
from database import get_session
from tasks.services import get_tasks_stats_by_day

router = APIRouter()


@router.get(
    "/stats/by-day",
    response_model=list[TasksStatsByDayItem],
    summary="Статистика задач по дням",
    description="Группировка задач текущего пользователя по дате создания.",
)
async def get_tasks_stats_by_day_endpoint(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> list[TasksStatsByDayItem]:
    rows = await get_tasks_stats_by_day(session=session, user_id=user_id)
    return [TasksStatsByDayItem(**row) for row in rows]
