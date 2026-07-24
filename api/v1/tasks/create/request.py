from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    title: Annotated[
        str,
        Field(description="Название задачи", examples=["Купить молоко"]),
        MinLen(3),
        MaxLen(255),
    ]
    description: Annotated[
        str | None,
        Field(description="Подробное описание (необязательно)", examples=["2 литра"]),
        MaxLen(500),
    ] = None
