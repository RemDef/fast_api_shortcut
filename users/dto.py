from dataclasses import dataclass
from datetime import date


@dataclass(slots=True, frozen=True)
class RegisterUserDTO:
    username: str
    email: str
    password: str
    first_name: str
    last_name: str
    birthdate: date
