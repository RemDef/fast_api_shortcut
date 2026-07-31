from pydantic import BaseModel, Field

from api.v1.tasks.active_users.response import ActiveUserItem
from api.v1.tasks.stats.by_day.response import TasksStatsByDayItem
from api.v1.tasks.stats.total.response import TasksStatsTotalResponse


class TasksDashboardResponse(BaseModel):
    total: TasksStatsTotalResponse = Field(description="Общая статистика задач")
    by_day: list[TasksStatsByDayItem] = Field(description="Статистика по дням")
    active_users: list[ActiveUserItem] = Field(
        description="Топ пользователей по открытым задачам"
    )
