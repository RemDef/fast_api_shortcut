from datetime import date
from typing import Self

from pydantic import BaseModel, Field

from tasks.dto import TasksStatsByDayDTO


class TasksStatsByDayItem(BaseModel):
    day: date = Field(description="Дата создания (день)")
    count: int = Field(description="Количество задач за день")

    @classmethod
    def from_dto(cls, dto: TasksStatsByDayDTO) -> Self:
        return cls(day=dto.day, count=dto.count)
