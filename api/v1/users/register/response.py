from datetime import date
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class RegisterUserResponse(BaseModel):
    id: Annotated[str, Field(description="Уникальный идентификатор пользователя")]
    username: Annotated[str, Field(description="Логин пользователя")]
    email: EmailStr = Field(description="Email пользователя")
    first_name: Annotated[str, Field(description="Имя")]
    last_name: Annotated[str, Field(description="Фамилия")]
    birthdate: date = Field(description="Дата рождения")
