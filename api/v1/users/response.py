from datetime import date, datetime

from typing import Annotated
from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    id: Annotated[
        str,
        Field(description="Уникальный идентификатор пользователя"),
    ]
    username: Annotated[
        str,
        Field(description="Логин пользователя", examples=["ivan_petrov"]),
    ]
    email: EmailStr = Field(
        description="Email пользователя", examples=["ivan@mail.com"]
    )
    first_name: Annotated[
        str,
        Field(description="Имя пользователя", examples=["Иван"]),
    ]
    last_name: Annotated[
        str,
        Field(description="Фамилия пользователя", examples=["Иванов"]),
    ]
    birthdate: date = Field(description="Дата рождения", examples=["1995-01-15"])
    created_at: Annotated[datetime, Field(description="Дата и время регистрации")]
    updated_at: Annotated[
        datetime, Field(description="Дата и время последнего обновления")
    ]
