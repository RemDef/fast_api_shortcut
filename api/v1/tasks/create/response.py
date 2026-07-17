from datetime import datetime

from pydantic import BaseModel, Field


class TaskResponse(BaseModel):
    id: str = Field(description="Уникальный идентификатор задачи")
    title: str = Field(description="Название задачи")
    description: str | None = Field(description="Описание задачи")
    is_done: bool = Field(description="Выполнена ли задача")
    created_at: datetime = Field(description="Дата и время создания")
    updated_at: datetime = Field(description="Дата и время последнего обновления")
