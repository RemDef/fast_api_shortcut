from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True, frozen=True)
class TaskDTO:
    id: str
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
    updated_at: datetime
