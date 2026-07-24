from datetime import datetime
from typing import Self

from pydantic import BaseModel, Field

from tasks.dto import TaskDTO


class TaskResponse(BaseModel):
    id: str = Field(description="Уникальный идентификатор задачи")
    title: str = Field(description="Название задачи")
    description: str | None = Field(description="Описание задачи")
    is_done: bool = Field(description="Выполнена ли задача")
    created_at: datetime = Field(description="Дата и время создания")
    updated_at: datetime = Field(description="Дата и время последнего обновления")

    @classmethod
    def from_dto(cls, dto: TaskDTO) -> Self:
        return cls(
            id=dto.id,
            title=dto.title,
            description=dto.description,
            is_done=dto.is_done,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
