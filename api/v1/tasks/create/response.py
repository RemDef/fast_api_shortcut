from datetime import datetime

from pydantic import BaseModel


class TaskResponse(BaseModel):
    id: str
    user_id: str
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
    updated_at: datetime
