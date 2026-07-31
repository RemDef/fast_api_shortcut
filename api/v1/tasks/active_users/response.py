from typing import Self

from pydantic import BaseModel, Field

from tasks.dto import ActiveUserDTO


class ActiveUserItem(BaseModel):
    user_id: str = Field(description="ID пользователя")
    username: str = Field(description="Логин")
    open_tasks: int = Field(description="Число невыполненных задач")

    @classmethod
    def from_dto(cls, dto: ActiveUserDTO) -> Self:
        return cls(
            user_id=dto.user_id,
            username=dto.username,
            open_tasks=dto.open_tasks,
        )
