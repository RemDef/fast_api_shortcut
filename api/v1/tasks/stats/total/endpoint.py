from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.auth.dependencies import get_current_user
from api.v1.tasks.stats.total.response import TasksStatsTotalResponse
from database import get_session
from tasks.services import get_tasks_stats_total

router = APIRouter()


@router.get(
    "/stats/total",
    response_model=TasksStatsTotalResponse,
    summary="Статистика задач",
    description="Количество выполненных/невыполненных задач и процент завершённых.",
)
async def get_tasks_stats_total_endpoint(
    user_id: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> TasksStatsTotalResponse:
    stats = await get_tasks_stats_total(session=session, user_id=user_id)
    return TasksStatsTotalResponse(**stats)
