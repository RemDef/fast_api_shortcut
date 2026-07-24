from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field


class UpdateTaskRequest(BaseModel):
    title: Annotated[
        str | None,
        Field(description="Название задачи", examples=["Купить молоко"]),
        MinLen(3),
        MaxLen(255),
    ] = None
    description: Annotated[
        str | None,
        Field(description="Подробное описание", examples=["2 литра"]),
        MaxLen(500),
    ] = None
    is_done: Annotated[
        bool | None,
        Field(description="Отметить задачу выполненной"),
    ] = None
