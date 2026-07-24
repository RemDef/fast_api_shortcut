from pydantic import BaseModel, Field


class TasksStatsTotalResponse(BaseModel):
    total: int = Field(description="Всего задач")
    done: int = Field(description="Выполненных задач")
    not_done: int = Field(description="Невыполненных задач")
    completion_percent: float = Field(description="Процент выполненных задач")
