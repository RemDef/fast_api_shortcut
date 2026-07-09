from datetime import date
from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr


class RegisterUserRequest(BaseModel):
    username: Annotated[str, MinLen(3), MaxLen(50)]
    email: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(128)]
    first_name: Annotated[str, MinLen(1), MaxLen(50)]
    last_name: Annotated[str, MinLen(1), MaxLen(50)]
    birthdate: date
