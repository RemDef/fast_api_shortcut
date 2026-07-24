from pydantic import BaseModel, Field


class TasksStatsByDayItem(BaseModel):
    day: str = Field(description="Дата создания (день)")
    count: int = Field(description="Количество задач за день")
