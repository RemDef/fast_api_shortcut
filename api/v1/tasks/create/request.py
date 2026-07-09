from typing import Annotated
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel


class CreateTaskRequest(BaseModel):
    title: Annotated[str, MinLen(3), MaxLen(255)]
    description: Annotated[str | None, MaxLen(500)] = None
