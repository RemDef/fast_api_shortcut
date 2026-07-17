from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, Field


class UpdateTaskRequest(BaseModel):
    title: Annotated[
        str | None,
        Field(
            description="Название задачи (необязательно)", examples=["Купить молоко"]
        ),
        MinLen(3),
        MaxLen(255),
    ] = None
    description: Annotated[
        str | None,
        Field(description="Подробное описание (необязательно)", examples=["2 литра"]),
        MaxLen(500),
    ] = None
    is_done: Annotated[
        bool | None,
        Field(description="Отметить задачу выполненной"),
    ] = None
