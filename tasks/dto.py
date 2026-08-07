from dataclasses import dataclass
from datetime import date, datetime
from uuid import UUID


@dataclass(slots=True, frozen=True)
class TaskDTO:
    id: UUID
    title: str
    description: str | None
    is_done: bool
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True, frozen=True)
class TasksStatsByDayDTO:
    day: date
    count: int


@dataclass(slots=True, frozen=True)
class TasksStatsTotalDTO:
    total: int
    done: int
    not_done: int
    completion_percent: float


@dataclass(slots=True, frozen=True)
class ActiveUserDTO:
    user_id: UUID
    username: str
    open_tasks: int
