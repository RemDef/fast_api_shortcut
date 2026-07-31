from pydantic import BaseModel, Field

from api.v1.tasks.common.schemas import TaskResponse


class PaginatedTasksResponse(BaseModel):
    count: int = Field(description="Всего задач по текущему фильтру")
    next: str | None = Field(description="URL следующей страницы")
    previous: str | None = Field(description="URL предыдущей страницы")
    results: list[TaskResponse] = Field(description="Задачи текущей страницы")
