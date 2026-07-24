from datetime import date
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import AfterValidator, BaseModel, EmailStr, Field

from users.security import validate_password_strength


def _years_ago(years: int) -> date:
    today = date.today()
    try:
        return today.replace(year=today.year - years)
    except ValueError:
        return today.replace(year=today.year - years, day=28)


def validate_birthdate(value: date) -> date:
    if value > _years_ago(14):
        raise ValueError("Пользователь должен быть не моложе 14 лет")
    if value < _years_ago(120):
        raise ValueError("Пользователь должен быть не старше 120 лет")
    return value


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
        str,
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
    birthdate: Annotated[
        date,
        Field(description="Дата рождения", examples=["1995-01-15"]),
        AfterValidator(validate_birthdate),
    ]
