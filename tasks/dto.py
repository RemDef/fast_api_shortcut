from dataclasses import dataclass
from datetime import date, datetime


@dataclass(slots=True, frozen=True)
class TaskDTO:
    id: str
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
    user_id: str
    username: str
    open_tasks: int
