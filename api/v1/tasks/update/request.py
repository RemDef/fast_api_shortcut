from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class UpdateTaskRequest(BaseModel):
    title: Annotated[str | None, MinLen(3), MaxLen(255)] = None
    description: Annotated[str | None, MaxLen(500)] = None
    is_done: bool | None = None
