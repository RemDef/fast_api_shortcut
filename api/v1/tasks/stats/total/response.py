from typing import Self

from pydantic import BaseModel, Field

from tasks.dto import TasksStatsTotalDTO


class TasksStatsTotalResponse(BaseModel):
    total: int = Field(description="Всего задач")
    done: int = Field(description="Выполненных задач")
    not_done: int = Field(description="Невыполненных задач")
    completion_percent: float = Field(description="Процент выполненных задач")

    @classmethod
    def from_dto(cls, dto: TasksStatsTotalDTO) -> Self:
        return cls(
            total=dto.total,
            done=dto.done,
            not_done=dto.not_done,
            completion_percent=dto.completion_percent,
        )
