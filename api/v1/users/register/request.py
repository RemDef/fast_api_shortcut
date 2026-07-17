from datetime import date
from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import AfterValidator, BaseModel, EmailStr, Field, SecretStr
from api.v1.users.validators import validate_password_strength


class RegisterUserRequest(BaseModel):
    username: Annotated[
        str,
        Field(description="Логин пользователя", examples=["ivan_petrov"]),
        MinLen(3),
        MaxLen(50),
    ]
    email: EmailStr = Field(
        description="Email пользователя", examples=["ivan@mail.com"]
    )
    password: Annotated[
        SecretStr,
        Field(
            description="Пароль должен содержать как минимум одну заглавную "
            "букву, строчную букву, цифру и спецсимвол"
        ),
        MinLen(8),
        MaxLen(128),
        AfterValidator(validate_password_strength),
    ]
    first_name: Annotated[
        str,
        Field(description="Имя пользователя", examples=["Иван"]),
        MinLen(1),
        MaxLen(50),
    ]
    last_name: Annotated[
        str,
        Field(description="Фамилия пользователя", examples=["Иванов"]),
        MinLen(1),
        MaxLen(50),
    ]
    birthdate: date = Field(description="Дата рождения", examples=["1995-01-15"])
