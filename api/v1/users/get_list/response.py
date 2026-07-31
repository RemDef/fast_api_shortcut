from pydantic import BaseModel, Field

from api.v1.users.common.schemas import UserResponse


class PaginatedUsersResponse(BaseModel):
    count: int = Field(description="Всего пользователей")
    next: str | None = Field(description="URL следующей страницы")
    previous: str | None = Field(description="URL предыдущей страницы")
    results: list[UserResponse] = Field(description="Пользователи текущей страницы")
