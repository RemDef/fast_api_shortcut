from pydantic import BaseModel, Field


class ActiveUserItem(BaseModel):
    user_id: str = Field(description="ID пользователя")
    username: str = Field(description="Логин")
    open_tasks: int = Field(description="Число невыполненных задач")
