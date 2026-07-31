from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TaskQuery(BaseModel):
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Сколько задач вернуть",
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Сколько задач пропустить",
    )
    is_done: bool | None = Field(
        default=None,
        description="Фильтр по статусу: true — выполненные, false — активные",
    )
    created_from: datetime | None = Field(
        default=None,
        description="Задачи, созданные не раньше этой даты",
    )
    created_to: datetime | None = Field(
        default=None,
        description="Задачи, созданные не позже этой даты",
    )
    order_by: Literal["created_at", "updated_at", "title"] = Field(
        default="created_at",
        description="Поле для сортировки",
    )
    direction: Literal["asc", "desc"] = Field(
        default="desc",
        description="Направление сортировки",
    )
    search: str | None = Field(
        default=None,
        alias="query",
        min_length=1,
        max_length=100,
        description="Поиск по подстроке в названии и описании",
    )
