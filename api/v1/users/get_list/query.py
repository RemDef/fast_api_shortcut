from pydantic import BaseModel, Field


class UserQuery(BaseModel):
    limit: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Сколько пользователей вернуть",
    )
    offset: int = Field(
        default=0,
        ge=0,
        description="Сколько пользователей пропустить",
    )
