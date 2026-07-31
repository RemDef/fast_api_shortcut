from dataclasses import dataclass
from datetime import date, datetime


@dataclass(slots=True, frozen=True)
class RegisterUserDTO:
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    birthdate: date


@dataclass(slots=True, frozen=True)
class UserDTO:
    id: str
    username: str
    email: str
    first_name: str
    last_name: str
    birthdate: date
    created_at: datetime
    updated_at: datetime
    is_admin: bool
